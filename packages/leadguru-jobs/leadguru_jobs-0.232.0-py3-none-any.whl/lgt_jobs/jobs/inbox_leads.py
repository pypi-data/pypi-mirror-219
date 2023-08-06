from abc import ABC
from lgt.common.python.lgt_logging import log
from lgt.common.python.slack_client.web_client import SlackWebClient
from lgt_data.enums import DefaultBoards
from lgt_data.model import UserModel, DedicatedBotModel, SlackMemberInformation, LeadModel, UserLeadModel
from lgt_data.mongo_repository import UserLeadMongoRepository, UserMongoRepository, DedicatedBotRepository, \
    SlackContactUserRepository, BoardsMongoRepository
from pydantic import BaseModel
from ..basejobs import BaseBackgroundJob, BaseBackgroundJobData
from ..services.web_client import V3ServerClient

"""
Save inbox leads
"""


class InboxLeadsJobData(BaseBackgroundJobData, BaseModel):
    pass


class InboxLeadsJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return InboxLeadsJobData

    def exec(self, _: InboxLeadsJobData):
        users = UserMongoRepository().get_users()
        for user in users:
            dedicated_bots = DedicatedBotRepository().get_user_bots(user.id, only_valid=True)
            for dedicated_bot in dedicated_bots:
                InboxLeadsJob.create_inbox_leads(user, dedicated_bot)

    @staticmethod
    def create_inbox_leads(user: UserModel, dedicated_bot: DedicatedBotModel):
        inbox_board = BoardsMongoRepository().get(user.id, is_primary=True, name=DefaultBoards.Inbox.value)
        if not inbox_board:
            return
        slack_client = SlackWebClient(dedicated_bot.token, dedicated_bot.cookies)
        v3_client = V3ServerClient()
        conversations_list = slack_client.get_im_list()
        for conversation in conversations_list.get('channels', []):
            sender_id = conversation.get('user')
            im_id = conversation.get('id')
            if sender_id == "USLACKBOT":
                continue
            log.warning(f'Loading chat for the: {dedicated_bot.id}')
            history = slack_client.chat_history(im_id)
            if not history['ok']:
                log.warning(f'Failed to load chat for the: {dedicated_bot.id}. ERROR: {history.get("error", "")}')
                continue

            messages = history.get('messages', [])
            if messages:
                user_lead = UserLeadMongoRepository().get_lead(user.id, sender_id=sender_id)
                if not user_lead:
                    people = SlackContactUserRepository().find_one(sender_id)
                    if not people:
                        slack_profile = slack_client.get_profile(sender_id).get('user')
                        InboxLeadsJob.create_people(slack_profile, dedicated_bot.name)

                    lead = UserLeadModel.from_dic(v3_client.save_lead_from_contact(sender_id, user.email))
                    v3_client.update_user_lead(lead.message.message_id, user.email,
                                               im_id, str(inbox_board[0].id), "Received")
                    log.info(f"[LoadChatHistoryJob]: Added inbox lead {lead.id} for user: {user.email}")

    @staticmethod
    def create_people(slack_profile: dict, workspace_name: str):
        member_info: SlackMemberInformation = SlackMemberInformation.from_slack_response(slack_profile, workspace_name)
        SlackContactUserRepository().collection().update_one({"user": member_info.user, "workspace": workspace_name},
                                                             {"$set": member_info.to_dic()}, upsert=True)
        return SlackContactUserRepository().find_one(member_info.user)
