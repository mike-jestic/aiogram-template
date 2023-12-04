from tortoise import fields
from tortoise.models import Model
from typing import Optional, Union, List
from tortoise import Tortoise
from dataclasses import dataclass


class Metric(Model):
    id = fields.IntField(pk=True, unique=True)
    code = fields.TextField()
    description = fields.TextField()

    users: fields.ReverseRelation["BotUser"]

    @classmethod
    async def get_metrics(cls):
        query = """
            SELECT m.code AS code, m.description AS desc, COUNT(u.id) AS count
            FROM metrics AS m
            LEFT JOIN bot_users AS u ON m.id = u.metric_id
            GROUP BY m.id;
        """
        metrics = await Tortoise.get_connection('default').execute_query_dict(query)
        
        return metrics
    
    class Meta:
        table = 'metrics'

class BotUser(Model):
    id = fields.BigIntField(pk=True)
    username = fields.TextField(null=True)
    admin = fields.BooleanField(default=False)
    time_reg = fields.DatetimeField(auto_now_add=True)
    metric: fields.ForeignKeyRelation[Metric] = fields.ForeignKeyField(
        "models.Metric", on_delete=fields.CASCADE, related_name="metric", null=True
    )
    referrer: fields.ForeignKeyRelation['BotUser'] = fields.ForeignKeyField(
        'models.BotUser', on_delete=fields.SET_NULL, null=True
    )
    active = fields.BooleanField(default=True)
    is_banned = fields.BooleanField(default=False)

    @property
    def url(self) -> str:
        url = f'<a href="{self.id}">*ссылка*</a>'
        if self.username: url = '@' + self.username
        return url
    
    @classmethod
    async def get_user(cls, query: Union[int, str]) -> 'BotUser':
        if isinstance(query, int):
            field = 'id'
        else:
            query = query.replace('@', '').replace('https://t.me/', '')
            field = 'id' if query.isdecimal() else 'username'
        user =  await cls.get_or_none(**{field: query})

        return user

    @classmethod
    async def get_top_referrers(cls) -> List['UserReferralData']:
        query = """
            SELECT t1.id AS user_id, COUNT(t2.id) AS count
            FROM bot_users AS t1
            LEFT JOIN bot_users AS t2 ON t1.id = t2.referrer_id
            GROUP BY t1.id
            ORDER BY count DESC
            LIMIT 5;
        """

        result = await Tortoise.get_connection('default').execute_query_dict(query)
        user_ids = [row['user_id'] for row in result]

        top_referrers = await BotUser.filter(id__in=user_ids)

        users_dict = {user.id: user for user in top_referrers}

        refs = []
        for row in result:

            refs.append(
                UserReferralData(
                    users_dict.get(
                        row['user_id']
                    ),
                    row['count']
                )
            )

        return refs


    class Meta:
        table = 'bot_users'


@dataclass
class UserReferralData:
    user: BotUser
    referral_count: int

# class ModelFields(Model):
#     id = fields.IntField(pk=True, unique=True)
#     need_comment = fields.BooleanField(default=False)

#     id = fields.BigIntField(pk=True, unique=True)
#     time_start = fields.DatetimeField(auto_now_add=True)
#     time_finish = fields.DatetimeField(null=True)

#     address: fields.ReverseRelation["ChecksOption"]
#     option: fields.ForeignKeyRelation["ChecksOption"] = fields.ForeignKeyField(
#         "models.ChecksOption", on_delete='CASCADE', related_name="option_orders"
#     )
#     comment = fields.TextField(default='')
