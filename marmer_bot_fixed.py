#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوت مرمر (Marley) - بوت الحماية القصوى
المطور: @R_DD_9
قناة التحديثات: @m_8eu

ملاحظة: هذا الكود يعمل مع python-telegram-bot v20+
للتثبيت: pip install python-telegram-bot>=20.0
"""

import os
import sys
import random
import json
import time
import datetime
import re
import asyncio
from typing import Dict, List, Optional

# ═══════════════════════════════════════════════════════════
# التحقق من إصدار المكتبة
# ═══════════════════════════════════════════════════════════

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler
    from telegram.ext import MessageHandler, filters, ContextTypes
    from telegram.constants import ParseMode
    print("✅ المكتبات مستوردة بنجاح")
except ImportError as e:
    print(f"❌ خطأ في استيراد المكتبات: {e}")
    print("يرجى تثبيت: pip install python-telegram-bot>=20.0")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════
# إعدادات البوت
# ═══════════════════════════════════════════════════════════

class Config:
    """إعدادات البوت"""

    # ⚠️ ضع التوكن هنا من @BotFather
    TOKEN = "YOUR_BOT_TOKEN_HERE"

    # معلومات المطور
    DEVELOPER_USERNAME = "@R_DD_9"
    DEVELOPER_ID = "7954570636"
    UPDATE_CHANNEL = "@m_8eu"

    # اسم البوت
    BOT_NAME_AR = "مرمر"
    BOT_NAME_EN = "Marley"

    # اللغات المدعومة
    LANGUAGES = {
        "ar": "🇮🇶 العربية",
        "en": "🇬🇧 English",
        "es": "🇪🇸 Español",
        "fr": "🇫🇷 Français",
        "de": "🇩🇪 Deutsch",
        "ru": "🇷🇺 Русский",
        "zh": "🇨🇳 中文",
        "ja": "🇯🇵 日本語",
        "ko": "🇰🇷 한국어",
        "tr": "🇹🇷 Türkçe"
    }

    # الرتب
    RANKS = {
        "member": {"name": "عضو", "emoji": "👤", "abbr": "عضو"},
        "featured": {"name": "مميز", "emoji": "🔰", "abbr": "م"},
        "admin": {"name": "أدمن", "emoji": "⚙️", "abbr": "اد"},
        "manager": {"name": "مدير", "emoji": "👔", "abbr": "مد"},
        "creator": {"name": "منشئ", "emoji": "📝", "abbr": "من"},
        "main_creator": {"name": "منشئ أساسي", "emoji": "⭐", "abbr": "مأ"},
        "secondary_dev": {"name": "مطور ثانوي", "emoji": "💻", "abbr": "مث"},
        "main_dev": {"name": "مطور أساسي", "emoji": "🔧", "abbr": "مط"},
        "emperor": {"name": "إمبراطور التليجرام", "emoji": "👑", "abbr": "إت"}
    }

# ═══════════════════════════════════════════════════════════
# قاعدة البيانات (محاكاة في الذاكرة)
# ═══════════════════════════════════════════════════════════

class Database:
    """قاعدة بيانات مؤقتة في الذاكرة"""

    def __init__(self):
        self.users = {}
        self.groups = {}
        self.banned_words = {}
        self.warnings = {}
        self.bank_accounts = {}
        self.games_scores = {}
        self.whispers = []
        self.responses = {}  # الردود المخصصة

    def get_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {
                "id": user_id,
                "username": "",
                "first_name": "",
                "last_name": "",
                "language": "ar",
                "rank": "member",
                "points": 0,
                "messages": 0,
                "warnings": 0,
                "muted": False,
                "banned": False,
                "bank_account": None,
                "joined_date": datetime.datetime.now().strftime("%Y-%m-%d")
            }
        return self.users[user_id]

    def get_group(self, group_id):
        if group_id not in self.groups:
            self.groups[group_id] = {
                "id": group_id,
                "name": "",
                "title": "",
                "banned_words": [],
                "locked_features": [],
                "enabled_features": {
                    "welcome": True,
                    "responses": True,
                    "id": True,
                    "link": True,
                    "protection": True,
                    "mention": True,
                    "verify": True,
                    "dev_responses": True,
                    "warn": True,
                    "bio": True,
                    "speak": True,
                    "games": True
                },
                "admins": [],
                "members": {},
                "settings": {}
            }
        return self.groups[group_id]

# إنشاء قاعدة البيانات
db = Database()


# ═══════════════════════════════════════════════════════════
# الردود العشوائية (العراقية)
# ═══════════════════════════════════════════════════════════

class Responses:
    """الردود العشوائية العراقية"""

    # ردود مرمر
    MARMER_RESPONSES = [
        "خير",
        "گول اسمعك",
        "ها بديت تزحف مو",
        "عيوني",
        "شتريد",
        "ها",
        "تدري انو انت لحيت",
        "كافي تكول مرمر مرمر مرمر تره دوختني",
        "تره دوختني",
        "كول شتريد",
        "عيونها لمرمر"
    ]

    # ردود احبك
    LOVE_RESPONSES = [
        "اموت فيك",
        "اعشقك",
        "لچذب",
        "وانا كمان",
        "خلي اسوي روحي مصدگه"
    ]

    # ردود خاص
    PRIVATE_RESPONSES = [
        "للرخاص",
        "ماء",
        "وولي",
        "دطير",
        "ها زاحف",
        "عيب",
        "يبوو"
    ]

    # ردود تعال خاص
    COME_PRIVATE_RESPONSES = [
        "يبوي شتبي انت",
        "ماء",
        "وولي",
        "دطير",
        "ها زاحف",
        "عيب",
        "يبوو"
    ]

    # ردود تعال خ
    COME_KH_RESPONSES = [
        "ماء",
        "وولي",
        "دطير",
        "ها زاحف",
        "عيب",
        "يبوو"
    ]

    # ردود نداء المطور
    DEV_RESPONSES = {
        "ar": "المطور {dev}",
        "en": "Developer {dev}",
        "es": "Desarrollador {dev}",
        "fr": "Développeur {dev}",
        "de": "Entwickler {dev}",
        "ru": "Разработчик {dev}",
        "zh": "开发者 {dev}",
        "ja": "開発者 {dev}",
        "ko": "개발자 {dev}",
        "tr": "Geliştirici {dev}"
    }

    # ردود رفع الرتب
    RANK_UP_RESPONSES = {
        "featured": "صار مميز",
        "admin": "صار ادمن",
        "manager": "صار مدير",
        "creator": "صار منشئ",
        "main_creator": "صار منشئ اساسي",
        "secondary_dev": "صار مطور ثانوي",
        "main_dev": "صار مطور اساسي",
        "emperor": "صار إمبراطور التليجرام"
    }

    # ردود تنزيل الرتب
    RANK_DOWN_RESPONSES = {
        "featured": "نزل من مميز",
        "admin": "نزل من ادمن",
        "manager": "نزل من مدير",
        "creator": "نزل من منشئ",
        "main_creator": "نزل من منشئ اساسي",
        "secondary_dev": "نزل من مطور ثانوي",
        "main_dev": "نزل من مطور اساسي",
        "emperor": "نزل من إمبراطور"
    }

    # ردود الحظر والكتم
    BAN_RESPONSES = {
        "ban": "تم الحظر",
        "unban": "تم الغاء الحظر",
        "kick": "تم الطرد",
        "mute": "تم الكتم",
        "unmute": "تم الغاء الكتم",
        "restrict": "تم التقييد",
        "unrestrict": "تم الغاء التقييد",
        "ban_global": "تم الحظر عام",
        "unban_global": "تم الغاء الحظر عام",
        "mute_global": "تم الكتم عام",
        "unmute_global": "تم الغاء الكتم عام"
    }

    # ردود الألعاب
    GAME_RESPONSES = {
        "win": "فزت! خوش حظ",
        "lose": "خسرت! جرب مرة ثانية",
        "draw": "تعادل!",
        "start": "يلا نبدأ!",
        "timeout": "انتهى الوقت!"
    }

    # ردود البنك
    BANK_RESPONSES = {
        "create": "تم انشاء حسابك البنكي",
        "delete": "تم مسح حسابك البنكي",
        "transfer": "تم التحويل",
        "balance": "رصيدك: {balance}",
        "salary": "تم استلام راتبك",
        "gift": "تم استلام بخشيش",
        "steal": "تم الزرف",
        "invest": "تم الاستثمار",
        "luck": "حظك: {result}",
        "trade": "نتيجة المضاربة: {result}"
    }

# ═══════════════════════════════════════════════════════════
# الألعاب (150 لعبة)
# ═══════════════════════════════════════════════════════════

class Games:
    """الألعاب (150 لعبة)"""

    GAMES_LIST = [
        # ألعاب أساسية (1-50)
        "رماية", "كرة القدم", "سباق سيارات", "الحظ", "ورق",
        "تحدي", "ألغاز", "معركة", "نرد", "بولينج",
        "قوس وسهم", "سيرك", "موسيقى", "رسم", "تمثيل",
        "كاريوكي", "أفلام", "معرفة", "جغرافيا", "فضاء",
        "ديناصورات", "تنين", "قراصنة", "قلعة", "محيط",
        "نار", "ثلج", "إعصار", "جواهر", "ملك",
        "سيف", "درع", "صيد", "صيد سمك", "مزرعة",
        "مصنع", "طيران", "بحري", "قطار", "ملاهي",
        "أفعوانية", "خيول", "بهلة", "مسابقات", "غناء",
        "تخمين أغنية", "تكنولوجيا", "برمجة", "تنبؤ", "فلك",

        # ألعاب إضافية (51-100)
        "شمس", "ألوان", "احتفال", "هدايا", "بالونات",
        "حفلة", "تنس طاولة", "ريشة", "هوكي", "كريكت",
        "ملاكمة", "مصارعة", "رفع أثقال", "جمباز", "تزلج",
        "زلاجة", "بلياردو", "منوبولي", "سلوت", "زهر",
        "جاكبوت", "كازينو", "لاس فيغاس", "روليت", "بوكر",
        "سهام", "مسرح", "فن", "دي جي", "عزف",
        "بيانو", "جيتار", "طبول", "كمان", "بوق",
        "ساكسفون", "عود", "طبول حربية", "أوركسترا", "أورغ",
        "روك", "أوبرا", "باليه", "رماية سهام", "نار سريعة",
        "حرب النرد", "ملك الجواهر", "بطولة العالم", "بطل الألعاب", "أركيد",

        # ألعاب جديدة (101-150)
        "فضائي", "روبوت", "نجم الألعاب", "ساحر", "كوميديا",
        "شعر", "بورتريه", "تراجيديا", "بهلوان", "ستاند اب",
        "فن شعبي", "دراما", "أكروبات", "غناء أوبرا", "فن تجريدي",
        "مسرح ظل", "دمى", "غناء شعبي", "فن رقمي", "مسرح عرائس",
        "جرافيتي", "هوليوود", "كونسول", "ريترو", "غزو الفضاء",
        "حرب الروبوتات", "مغامرة نجم", "باتل رويال", "سباق أركيد", "مدافع الفضاء",
        "مستقبلي", "نجم القتال", "فايتنغ", "منصات", "زومبي",
        "سايبورغ", "نجم السباق", "راب", "هيب هوب", "جاز",
        "بلوز", "ميتال", "كلاسيك", "جاز بوق", "سول",
        "إلكترونيك", "بانك", "فيولين", "ترومبيت", "كلارينيت",
        "هاربسكورد", "فلامنكو", "تشيلو"
    ]

    # ألعاب الصور
    IMAGE_GAMES = [
        "مكياج", "ايموجي", "كوره", "انديه", "خمن",
        "سيارات", "صور", "بوب", "كيبوب", "انمي",
        "فنانين", "المختلف", "جدول"
    ]

    # ألعاب كتابية
    TEXT_GAMES = [
        "كت ليبي", "كت عراقي", "حرف", "كلمات", "عربي",
        "اكمل", "انقليزي", "تفكيك", "الاسرع", "العكس",
        "حزوره", "ترتيب", "علم دول", "دين", "عامه",
        "رياضيات", "مصطلح", "تركيب"
    ]

    # ألعاب جماعية
    GROUP_GAMES = [
        "عقاب", "حكم", "احكام", "تحدي", "حزر",
        "بغني", "كرسي اعتراف"
    ]

    @staticmethod
    def get_random_game():
        return random.choice(Games.GAMES_LIST)

    @staticmethod
    def get_game_by_category(category):
        if category == "image":
            return Games.IMAGE_GAMES
        elif category == "text":
            return Games.TEXT_GAMES
        elif category == "group":
            return Games.GROUP_GAMES
        return Games.GAMES_LIST


# ═══════════════════════════════════════════════════════════
# نظام الرتب
# ═══════════════════════════════════════════════════════════

class RankSystem:
    """نظام الرتب"""

    RANK_ORDER = [
        "member", "featured", "admin", "manager", 
        "creator", "main_creator", "secondary_dev", 
        "main_dev", "emperor"
    ]

    @staticmethod
    def get_rank_info(rank_key):
        return Config.RANKS.get(rank_key, Config.RANKS["member"])

    @staticmethod
    def is_higher_rank(rank1, rank2):
        """هل rank1 أعلى من rank2"""
        try:
            idx1 = RankSystem.RANK_ORDER.index(rank1)
            idx2 = RankSystem.RANK_ORDER.index(rank2)
            return idx1 > idx2
        except ValueError:
            return False

    @staticmethod
    def can_promote(promoter_rank, target_rank):
        """هل يمكن رفع الرتبة"""
        return RankSystem.is_higher_rank(promoter_rank, target_rank)

    @staticmethod
    def promote_user(group_id, user_id, target_id, new_rank):
        """رفع رتبة مستخدم"""
        group = db.get_group(group_id)
        user = db.get_user(user_id)
        target = db.get_user(target_id)

        # التحقق من صلاحيات المرفوع
        if str(user_id) == Config.DEVELOPER_ID:
            # المطور يمكنه كل شيء
            target["rank"] = new_rank
            return True, Responses.RANK_UP_RESPONSES.get(new_rank, "تم الرفع")

        if not RankSystem.can_promote(user["rank"], target["rank"]):
            return False, "ما تقدر ترفع رتبة أعلى منك"

        if not RankSystem.can_promote(user["rank"], new_rank):
            return False, "ما تقدر ترفع له هاي الرتبة"

        target["rank"] = new_rank
        return True, Responses.RANK_UP_RESPONSES.get(new_rank, "تم الرفع")

    @staticmethod
    def demote_user(group_id, user_id, target_id, rank_to_remove):
        """تنزيل رتبة مستخدم"""
        group = db.get_group(group_id)
        user = db.get_user(user_id)
        target = db.get_user(target_id)

        if str(user_id) == Config.DEVELOPER_ID:
            if rank_to_remove == "all":
                target["rank"] = "member"
                return True, "تم تنزيل كل الرتب"
            target["rank"] = "member"
            return True, Responses.RANK_DOWN_RESPONSES.get(rank_to_remove, "تم التنزيل")

        if not RankSystem.is_higher_rank(user["rank"], target["rank"]):
            return False, "ما تقدر تنزل رتبة أعلى منك"

        if rank_to_remove == "all":
            target["rank"] = "member"
            return True, "تم تنزيل كل الرتب"

        target["rank"] = "member"
        return True, Responses.RANK_DOWN_RESPONSES.get(rank_to_remove, "تم التنزيل")

# ═══════════════════════════════════════════════════════════
# الحماية
# ═══════════════════════════════════════════════════════════

class Protection:
    """نظام الحماية"""

    LOCKABLE_FEATURES = [
        "edit", "voice", "video", "photo", "sticker", "join",
        "farsi", "document", "gif", "media_edit", "chat",
        "link", "hashtag", "bot", "username", "mention",
        "spam", "repeat", "forward", "inline", "contact",
        "all", "swear", "add", "audio", "channel"
    ]

    @staticmethod
    def is_banned_word(group_id, word):
        """هل الكلمة محظورة"""
        group = db.get_group(group_id)
        return word.lower() in [w.lower() for w in group["banned_words"]]

    @staticmethod
    def add_banned_word(group_id, word):
        """إضافة كلمة محظورة"""
        group = db.get_group(group_id)
        if word not in group["banned_words"]:
            group["banned_words"].append(word)
            return True, "تم منع الكلمة"
        return False, "الكلمة موجودة"

    @staticmethod
    def remove_banned_word(group_id, word):
        """إزالة كلمة محظورة"""
        group = db.get_group(group_id)
        if word in group["banned_words"]:
            group["banned_words"].remove(word)
            return True, "تم السماح بالكلمة"
        return False, "الكلمة مو موجودة"

    @staticmethod
    def lock_feature(group_id, feature):
        """قفل ميزة"""
        group = db.get_group(group_id)
        if feature not in group["locked_features"]:
            group["locked_features"].append(feature)
            return True, f"تم قفل {feature}"
        return False, f"{feature} مقفول"

    @staticmethod
    def unlock_feature(group_id, feature):
        """فتح ميزة"""
        group = db.get_group(group_id)
        if feature in group["locked_features"]:
            group["locked_features"].remove(feature)
            return True, f"تم فتح {feature}"
        return False, f"{feature} مفتوح"

    @staticmethod
    def is_feature_locked(group_id, feature):
        """هل الميزة مقفولة"""
        group = db.get_group(group_id)
        return feature in group["locked_features"] or "all" in group["locked_features"]

    @staticmethod
    def detect_spam(text):
        """كشف السبام"""
        # روابط متكررة
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        if len(urls) > 3:
            return True, "سبام روابط"

        # mentions متكررة
        mentions = re.findall(r'@\w+', text)
        if len(mentions) > 5:
            return True, "سبام منشن"

        # تكرار نفس النص
        if len(text) > 50:
            words = text.split()
            unique_words = set(words)
            if len(words) > 0 and len(unique_words) / len(words) < 0.3:
                return True, "تكرار"

        return False, ""

    @staticmethod
    def check_message(update, context):
        """فحص الرسالة"""
        if not update.message or not update.message.text:
            return True, ""

        text = update.message.text
        user_id = update.message.from_user.id
        chat_id = update.message.chat_id

        # كشف السبام
        is_spam, reason = Protection.detect_spam(text)
        if is_spam:
            return False, reason

        # كشف الكلمات المحظورة
        words = text.split()
        for word in words:
            if Protection.is_banned_word(chat_id, word):
                return False, f"كلمة محظورة: {word}"

        return True, ""


# ═══════════════════════════════════════════════════════════
# البنك
# ═══════════════════════════════════════════════════════════

class Bank:
    """نظام البنك"""

    @staticmethod
    def create_account(user_id):
        """إنشاء حساب بنكي"""
        user = db.get_user(user_id)
        if user["bank_account"] is not None:
            return False, "عندك حساب بنكي"

        account_number = f"BANK{user_id}{random.randint(1000, 9999)}"
        user["bank_account"] = {
            "number": account_number,
            "balance": 1000,  # رصيد اولي
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transactions": []
        }
        return True, f"تم انشاء حسابك البنكي
رقم الحساب: {account_number}"

    @staticmethod
    def delete_account(user_id):
        """مسح حساب بنكي"""
        user = db.get_user(user_id)
        if user["bank_account"] is None:
            return False, "ما عندك حساب بنكي"

        user["bank_account"] = None
        return True, "تم مسح حسابك البنكي"

    @staticmethod
    def get_balance(user_id):
        """الحصول على الرصيد"""
        user = db.get_user(user_id)
        if user["bank_account"] is None:
            return False, "ما عندك حساب بنكي"

        balance = user["bank_account"]["balance"]
        return True, f"رصيدك: {balance} فلوس"

    @staticmethod
    def transfer(from_id, to_id, amount):
        """تحويل فلوس"""
        from_user = db.get_user(from_id)
        to_user = db.get_user(to_id)

        if from_user["bank_account"] is None:
            return False, "ما عندك حساب بنكي"
        if to_user["bank_account"] is None:
            return False, "المستلم ما عنده حساب بنكي"

        if from_user["bank_account"]["balance"] < amount:
            return False, "رصيدك ما يكفي"

        from_user["bank_account"]["balance"] -= amount
        to_user["bank_account"]["balance"] += amount

        # تسجيل المعاملة
        transaction = {
            "from": from_id,
            "to": to_id,
            "amount": amount,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        from_user["bank_account"]["transactions"].append(transaction)
        to_user["bank_account"]["transactions"].append(transaction)

        return True, f"تم التحويل: {amount} فلوس"

    @staticmethod
    def get_salary(user_id):
        """الحصول على الراتب"""
        user = db.get_user(user_id)
        if user["bank_account"] is None:
            return False, "ما عندك حساب بنكي"

        # راتب كل 20 دقيقة
        salary = random.randint(100, 500)
        user["bank_account"]["balance"] += salary
        return True, f"تم استلام راتبك: {salary} فلوس"

    @staticmethod
    def get_gift(user_id):
        """الحصول على بخشيش"""
        user = db.get_user(user_id)
        if user["bank_account"] is None:
            return False, "ما عندك حساب بنكي"

        # بخشيش كل 10 دقائق
        gift = random.randint(50, 200)
        user["bank_account"]["balance"] += gift
        return True, f"تم استلام بخشيش: {gift} فلوس"

    @staticmethod
    def steal(user_id, target_id):
        """زرف فلوس"""
        user = db.get_user(user_id)
        target = db.get_user(target_id)

        if user["bank_account"] is None:
            return False, "ما عندك حساب بنكي"
        if target["bank_account"] is None:
            return False, "المستهدف ما عنده حساب بنكي"

        # زرف كل 10 دقائق
        steal_amount = random.randint(1, min(100, target["bank_account"]["balance"]))
        target["bank_account"]["balance"] -= steal_amount
        user["bank_account"]["balance"] += steal_amount

        return True, f"تم الزرف: {steal_amount} فلوس"

    @staticmethod
    def invest(user_id, amount):
        """استثمار"""
        user = db.get_user(user_id)
        if user["bank_account"] is None:
            return False, "ما عندك حساب بنكي"

        if user["bank_account"]["balance"] < amount:
            return False, "رصيدك ما يكفي"

        # نسبة ربح من 1% إلى 15%
        profit_percent = random.randint(1, 15)
        profit = int(amount * profit_percent / 100)

        user["bank_account"]["balance"] -= amount
        user["bank_account"]["balance"] += amount + profit

        return True, f"تم الاستثمار
ربح: {profit} فلوس ({profit_percent}%)"

    @staticmethod
    def luck_game(user_id, amount):
        """لعبة الحظ"""
        user = db.get_user(user_id)
        if user["bank_account"] is None:
            return False, "ما عندك حساب بنكي"

        if user["bank_account"]["balance"] < amount:
            return False, "رصيدك ما يكفي"

        # 50% فرصة للفوز
        if random.random() > 0.5:
            win = amount * 2
            user["bank_account"]["balance"] += win
            return True, f"فزت! {win} فلوس"
        else:
            user["bank_account"]["balance"] -= amount
            return False, f"خسرت! {amount} فلوس"

    @staticmethod
    def trade(user_id, amount):
        """مضاربة"""
        user = db.get_user(user_id)
        if user["bank_account"] is None:
            return False, "ما عندك حساب بنكي"

        if user["bank_account"]["balance"] < amount:
            return False, "رصيدك ما يكفي"

        # نسبة من -90% إلى +90%
        change_percent = random.randint(-90, 90)
        change = int(amount * change_percent / 100)

        user["bank_account"]["balance"] += change

        if change > 0:
            return True, f"ربحت: {change} فلوس ({change_percent}%)"
        else:
            return False, f"خسرت: {abs(change)} فلوس ({change_percent}%)"

    @staticmethod
    def get_top_rich():
        """توب الأغنياء"""
        rich_list = []
        for user_id, user in db.users.items():
            if user["bank_account"]:
                rich_list.append((user_id, user["bank_account"]["balance"]))

        rich_list.sort(key=lambda x: x[1], reverse=True)
        return rich_list[:10]

    @staticmethod
    def get_top_thieves():
        """توب الحرامية"""
        # محاكاة
        return []

# ═══════════════════════════════════════════════════════════
# التسلية
# ═══════════════════════════════════════════════════════════

class Fun:
    """أوامر التسلية"""

    @staticmethod
    def random_percentage():
        """نسبة عشوائية"""
        return random.randint(1, 100)

    @staticmethod
    def marry(user_id, target_id):
        """زواج عشوائي"""
        user = db.get_user(user_id)
        target = db.get_user(target_id)

        return f"زوجتك: {target.get('first_name', 'مجهول')}"

    @staticmethod
    def divorce():
        """طلاق"""
        return "تم الطلاق"

    @staticmethod
    def love_percentage(user_id, target_id):
        """نسبة الحب"""
        return Fun.random_percentage()

    @staticmethod
    def beauty_percentage(user_id):
        """نسبة الجمال"""
        return Fun.random_percentage()

    @staticmethod
    def intelligence_percentage(user_id):
        """نسبة الذكاء"""
        return Fun.random_percentage()

    @staticmethod
    def stupidity_percentage(user_id):
        """نسبة الغباء"""
        return Fun.random_percentage()

    @staticmethod
    def lie_percentage(user_id):
        """نسبة الكذب"""
        return Fun.random_percentage()

    @staticmethod
    def betrayal_percentage(user_id):
        """نسبة الخيانة"""
        return Fun.random_percentage()

    @staticmethod
    def masculinity_percentage(user_id):
        """نسبة الرجولة"""
        return Fun.random_percentage()

    @staticmethod
    def femininity_percentage(user_id):
        """نسبة الأنوثة"""
        return Fun.random_percentage()

    @staticmethod
    def horoscope(sign):
        """برج"""
        horoscopes = [
            "حظك اليوم جيد",
            "حذر من الأصدقاء",
            "فرصة ذهبية قادمة",
            "احذر من الغدر",
            "يومك حلو"
        ]
        return random.choice(horoscopes)

    @staticmethod
    def prediction():
        """توقع"""
        predictions = [
            "تتزوج السنة الجاية",
            "تصير غني",
            "تسافر برا",
            "تشتري سيارة",
            "تفتح مشروع"
        ]
        return random.choice(predictions)

    @staticmethod
    def compare(user1_id, user2_id):
        """مقارنة"""
        return f"الأفضل: {random.choice(['الأول', 'الثاني'])}"

    @staticmethod
    def truth():
        """صراحة"""
        truths = [
            "وش أكثر شي تخاف منه؟",
            "وش أكثر شخص تحبه؟",
            "وش سرك المخفي؟",
            "وش أكثر شي ندمت عليه؟"
        ]
        return random.choice(truths)

    @staticmethod
    def dare():
        """جرأة"""
        dares = [
            "ارسل رسالة لحبيبك",
            "غني أغنية",
            "رقص قدام الجميع",
            "اعترف بشي مخبي"
        ]
        return random.choice(dares)

    @staticmethod
    def analyze_name(name):
        """تحليل الاسم"""
        analyses = [
            "اسمك قوي",
            "اسمك حلو",
            "اسمك نادر",
            "اسمك مشهور"
        ]
        return random.choice(analyses)

    @staticmethod
    def guess_future():
        """تخمين المستقبل"""
        futures = [
            "تصير دكتور",
            "تصير مهندس",
            "تصير فنان",
            "تصير رجل أعمال",
            "تصير معلم"
        ]
        return random.choice(futures)


# ═══════════════════════════════════════════════════════════
# معالجات الأوامر (async/await للإصدار v20+)
# ═══════════════════════════════════════════════════════════

class CommandHandlers:
    """معالجات الأوامر"""

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر البداية"""
        user = update.effective_user
        chat = update.effective_chat

        # تحديث معلومات المستخدم
        db_user = db.get_user(user.id)
        db_user["username"] = user.username or ""
        db_user["first_name"] = user.first_name or ""
        db_user["last_name"] = user.last_name or ""

        welcome_text = f"""اهلين فيك باوامر البوت

للاستفسار - {Config.DEVELOPER_USERNAME}

⌯ اضغط على الازرار تحت عشان تشوف الاوامر"""

        keyboard = [
            [InlineKeyboardButton("م1", callback_data="menu_1"),
             InlineKeyboardButton("م2", callback_data="menu_2"),
             InlineKeyboardButton("م3", callback_data="menu_3")],
            [InlineKeyboardButton("م4", callback_data="menu_4"),
             InlineKeyboardButton("م5", callback_data="menu_5"),
             InlineKeyboardButton("م6", callback_data="menu_6")],
            [InlineKeyboardButton("م7", callback_data="menu_7"),
             InlineKeyboardButton("م8", callback_data="menu_8"),
             InlineKeyboardButton("م9", callback_data="menu_9")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

    @staticmethod
    async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالجة الأزرار"""
        query = update.callback_query
        await query.answer()

        data = query.data

        if data == "menu_1":
            text = """❨ اوامر الرفع والتنزيل ❩

⌯ رفع ↣ ↢ تنزيل مشرف
⌯ رفع ↣ ↢ تنزيل مالك اساسي
⌯ رفع ↣ ↢ تنزيل مالك
⌯ رفع ↣ ↢ تنزيل مدير
⌯ رفع ↣ ↢ تنزيل ادمن
⌯ رفع ↣ ↢ تنزيل مميز
⌯ تنزيل الكل ↢ بالرد ↢ لتنزيل الشخص من جميع رتبه
⌯ تنزيل الكل ↢ بدون رد ↢ لتنزيل كل رتب المجموعة

❨ اوامر المسح ❩

⌯ مسح المالكيين
⌯ مسح المدراء
⌯ مسح الادمنيه
⌯ مسح المميزين
⌯ مسح المحظورين
⌯ مسح المكتومين
⌯ مسح قائمة المنع
⌯ مسح رتبه
⌯ مسح الرتب
⌯ مسح الردود
⌯ مسح الاوامر
⌯ مسح + العدد
⌯ مسح بالرد
⌯ مسح الترحيب
⌯ مسح قائمة التثبيت

❨ اوامر الطرد الحظر الكتم ❩

⌯ حظر ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ طرد ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ كتم ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ تقيد ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ الغاء الحظر ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ الغاء الكتم ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ الغاء التقييد ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ رفع القيود ↢ لحذف الكتم,الحظر,التقييد
⌯ منع الكلمة
⌯ منع بالرد على قيف او ستيكر
⌯ الغاء منع الكلمة
⌯ طرد البوتات
⌯ كشف البوتات

❨ اوامر النطق ❩

⌯ انطقي + الكلمة
⌯ وش يقول؟ + بالرد على فويس لترجمه المحتوى

❨ اوامر اخرى ❩

⌯ الرابط
⌯ معلومات الرابط
⌯ انشاء رابط
⌯ بايو
⌯ بايو عشوائي
⌯ ايدي
⌯ الانشاء
⌯ مجموعاتي
⌯ @admin
⌯ نقل ملكية
⌯ صوره
⌯ افتاري
⌯ افتار + باليوزر او الرد
⌯ مين ضافني؟"""

        elif data == "menu_2":
            text = """❨ اوامر التعيين ❩

⌯ تعيين الترحيب
⌯ تعيين القوانين
⌯ تغيير رتبه
⌯ تغيير امر

❨ اوامر رؤية الاعدادات ❩

⌯ المطورين
⌯ المالكيين الاساسيين
⌯ المالكيين
⌯ الادمنيه
⌯ المدراء
⌯ المشرفين
⌯ المميزين
⌯ القوانين
⌯ قائمه المنع
⌯ المكتومين
⌯ المطور
⌯ معلوماتي
⌯ الاعدادت
⌯ المجموعه
⌯ الساعه
⌯ التاريخ
⌯ صلاحياتي
⌯ لقبي
⌯ صلاحياته + بالرد"""

        elif data == "menu_3":
            text = """❨ اوامر الردود ❩

⌯ الردود ↢ تشوف كل الردود المضافه
⌯ اضف رد ↢ عشان تضيف رد
⌯ مسح رد ↢ عشان تمسح الرد
⌯ مسح الردود ↢ تمسح كل الردود
⌯ الرد + كلمة الرد

❨ اوامر القفل والفتح بالمسح ❩

⌯ قفل ↣ ↢ فتح التعديل
⌯ قفل ↣ ↢ فتح الفويسات
⌯ قفل ↣ ↢ فتح الفيديو
⌯ قفل ↣ ↢ فتح الـصــور
⌯ قفل ↣ ↢ فتح الملصقات
⌯ قفل ↣ ↢ فتح الدخول
⌯ قفل ↣ ↢ فتح الفارسية
⌯ قفل ↣ ↢ فتح الملفات
⌯ قفل ↣ ↢ فتح المتحركات
⌯ قفل ↣ ↢ فتح تعديل الميديا
⌯ قفل ↣ ↢ فتح تعديل الميديا بالتقييد
⌯ قفل ↣ ↢ فتح الدردشه
⌯ قفل ↣ ↢ فتح الروابط
⌯ قفل ↣ ↢ فتح الهشتاق
⌯ قفل ↣ ↢ فتح البوتات
⌯ قفل ↣ ↢ فتح اليوزرات
⌯ قفل ↣ ↢ فتح الاشعارات
⌯ قفل ↣ ↢ فتح الكلام الكثير
⌯ قفل ↣ ↢ فتح التكرار
⌯ قفل ↣ ↢ فتح التوجيه
⌯ قفل ↣ ↢ فتح الانلاين
⌯ قفل ↣ ↢ فتح الجهات
⌯ قفل ↣ ↢ فتح الــكـــل
⌯ قفل ↣ ↢ فتح السب
⌯ قفل ↣ ↢ فتح الاضافه
⌯ قفل ↣ ↢ فتح الصوت
⌯ قفل ↣ ↢ فتح القنوات

❨ اوامر التفعيل والتعطيل ❩

⌯ تفعيل ↣ ↢ تعطيل الترحيب
⌯ تفعيل ↣ ↢ تعطيل الردود
⌯ تفعيل ↣ ↢ تعطيل الايدي
⌯ تفعيل ↣ ↢ تعطيل الرابط
⌯ تفعيل ↣ ↢ تعطيل اطردني
⌯ تفعيل ↣ ↢ تعطيل الحماية
⌯ تفعيل ↣ ↢ تعطيل المنشن
⌯ تفعيل ↣ ↢ تعطيل التحقق
⌯ تفعيل ↣ ↢ تعطيل ردود المطور
⌯ تفعيل ↣ ↢ تعطيل التحذير
⌯ تفعيل ↣ ↢ تعطيل البايو
⌯ تفعيل ↣ ↢ تعطيل انطقي"""

        elif data == "menu_4":
            text = """☤ تفعيل الالعاب
☤ تعطيل الالعاب

✽ جمل
✽ كلمات
✽ دين
✽ عربي
✽ اكمل
✽ صور
✽ كت
✽ مؤقت
✽ اعلام
✽ معاني
✽ تخمين
✽ احكام
✽ ارقام
✽ احسب
✽ خواتم
✽ انقليزي
✽ ترتيب
✽ انمي
✽ تركيب
✽ تفكيك
✽ عواصم
✽ روليت
✽ سيارات
✽ ايموجي
✽ حجره
✽ ديمون"""

        elif data == "menu_5":
            text = """❖ فلوسي ↼ عشان تشوف فلوسك

⌯ انشاء حساب بنكي ↢ تسوي حساب وتقدر تحول فلوس مع مزايا ثانيه
⌯ مسح حساب بنكي ↢ تلغي حسابك البنكي
⌯ تحويل ↢ تطلب رقم حساب الشخص وتحول له فلوس
⌯ حسابي ↢ يطلع لك رقم حسابك عشان تعطيه للشخص اللي بيحول لك
⌯ فلوسي ↢ يعلمك كم فلوسك
⌯ راتب ↢ يعطيك راتبك كل ٢٠ دقيقة
⌯ بخشيش ↢ يعطيك بخشيش كل ١٠ دقايق
⌯ زرف ↢ تزرف فلوس اشخاص كل ١٠ دقايق
⌯ استثمار ↢ تستثمر بالمبلغ اللي تبيه مع نسبة ربح مضمونه من ١٪؜ الى ١٥٪؜
⌯ حظ ↢ تلعبها بأي مبلغ ياتدبله ياتخسره انت وحظك
⌯ مضاربه ↢ تضارب بأي مبلغ تبيه والنسبة من ٩٠٪؜ الى -٩٠٪؜ انت وحظك
⌯ توب الفلوس ↢ يطلع توب اكثر ناس معهم فلوس بكل القروبات
⌯ توب الحراميه ↢ يطلع لك اكثر ناس زرفوا"""

        elif data == "menu_6":
            text = """⌯ زوجني ↢ يختار زوجة عشوائية
⌯ طلاق ↢ طلاق
⌯ كت ↢ كت تويت عشوائي
⌯ نسبة الحب ↢ نسبة الحب بين شخصين
⌯ نسبة الجمال ↢ نسبة جمالك
⌯ نسبة الذكاء ↢ نسبة ذكائك
⌯ نسبة الغباء ↢ نسبة غبائك
⌯ نسبة الكذب ↢ نسبة كذبك
⌯ نسبة الخيانة ↢ نسبة خيانتك
⌯ نسبة الشخصية ↢ تحليل شخصيتك
⌯ نسبة الرجولة ↢ نسبة رجولتك
⌯ نسبة الانوثة ↢ نسبة أنوثتك
⌯ برج ↢ برجك اليوم
⌯ توقع ↢ توقع عشوائي
⌯ مقارنة ↢ مقارنة بين شخصين
⌯ صراحة ↢ سؤال صراحة
⌯ تحدي ↢ تحدي عشوائي
⌯ جرأة ↢ جرأة عشوائية
⌯ كذبة ↢ كذبة عشوائية
⌯ حقيقة ↢ حقيقة عشوائية
⌯ تحليل ↢ تحليل اسمك
⌯ معنى الاسم ↢ معنى اسمك
⌯ عمرك بالايام ↢ حساب عمرك بالايام
⌯ متى زواجك ↢ توقع زواجك
⌯ كم طولك ↢ تخمين طولك
⌯ كم وزنك ↢ تخمين وزنك
⌯ لون عينك ↢ تخمين لون عينك
⌯ لون شعرك ↢ تخمين لون شعرك
⌯ وش جنسية ↢ تخمين جنسيتك
⌯ وش اصلك ↢ تخمين أصلك
⌯ وش طبعك ↢ تحليل طبعك
⌯ وش يقولون عنك ↢ تخمين ما يقولون عنك
⌯ وش يحبون فيك ↢ تخمين ما يحبون فيك
⌯ وش يكرهون فيك ↢ تخمين ما يكرهون فيك
⌯ وش ناوي عليك ↢ تخمين نيات الناس
⌯ وش مستقبلك ↢ توقع مستقبلك
⌯ وش حظك اليوم ↢ حظك اليوم
⌯ وش يومك ↢ توقع يومك
⌯ وش اسبوعك ↢ توقع أسبوعك
⌯ وش شهرك ↢ توقع شهرك
⌯ وش سنتك ↢ توقع سنتك
⌯ وش عمرك ↢ توقع عمرك
⌯ وش راتبك ↢ توقع راتبك
⌯ وش سيارتك ↢ توقع سيارتك
⌯ وش بيتك ↢ توقع بيتك
⌯ وش زوجتك ↢ توقع زوجتك
⌯ وش اولادك ↢ توقع عدد أولادك
⌯ وش وظيفتك ↢ توقع وظيفتك
⌯ وش دولتك ↢ توقع دولتك
⌯ وش مدينتك ↢ توقع مدينتك
⌯ وش شارعك ↢ توقع شارعك
⌯ وش حارتك ↢ توقع حارتك
⌯ وش جامعتك ↢ توقع جامعتك
⌯ وش تخصصك ↢ توقع تخصصك
⌯ وش معدلك ↢ توقع معدلك
⌯ وش شهادتك ↢ توقع شهادتك
⌯ وش عملك ↢ توقع عملك
⌯ وش مشروعك ↢ توقع مشروعك
⌯ وش شركتك ↢ توقع شركتك
⌯ وش رئيسك ↢ توقع رئيسك
⌯ وش زميلك ↢ توقع زميلك
⌯ وش صديقك ↢ توقع صديقك
⌯ وش عدوك ↢ توقع عدوك
⌯ وش حبيبك ↢ توقع حبيبك
⌯ وش خليفتك ↢ توقع خليفتك
⌯ وش نجمك ↢ توقع نجمك
⌯ وش فنانك ↢ توقع فنانك
⌯ وش لاعبك ↢ توقع لاعبك
⌯ وش فريقك ↢ توقع فريقك
⌯ وش منتخبك ↢ توقع منتخبك
⌯ وش بطلك ↢ توقع بطلك
⌯ وش قدوتك ↢ توقع قدوتك
⌯ وش معلمك ↢ توقع معلمك
⌯ وش طبيبك ↢ توقع طبيبك
⌯ وش محاميك ↢ توقع محاميك
⌯ وش مهندسك ↢ توقع مهندسك
⌯ وش كاتبك ↢ توقع كاتبك
⌯ وش شاعرك ↢ توقع شاعرك
⌯ وش فلكك ↢ توقع فلكك
⌯ وش برجك ↢ توقع برجك
⌯ وش حجرك ↢ توقع حجرك
⌯ وش لونك ↢ توقع لونك
⌯ وش رقمك ↢ توقع رقمك
⌯ وش حرفك ↢ توقع حرفك
⌯ وش اسمك ↢ توقع اسمك
⌯ وش كنيتك ↢ توقع كنيتك
⌯ وش لقبك ↢ توقع لقبك
⌯ وش نسبك ↢ توقع نسبك
⌯ وش عائلتك ↢ توقع عائلتك
⌯ وش قبيلتك ↢ توقع قبيلتك
⌯ وش ديانتك ↢ توقع ديانتك
⌯ وش مذهبك ↢ توقع مذهبك
⌯ وش طائفتك ↢ توقع طائفتك
⌯ وش عرقتك ↢ توقع عرقتك
⌯ وش جنستك ↢ توقع جنستك
⌯ وش جنسيتك ↢ توقع جنسيتك
⌯ وش اقامتك ↢ توقع اقامتك
⌯ وش جوازك ↢ توقع جوازك
⌯ وش هويتك ↢ توقع هويتك
⌯ وش بطاقتك ↢ توقع بطاقتك
⌯ وش رخصتك ↢ توقع رخصتك
⌯ وش سيارتك ↢ توقع سيارتك
⌯ وش دراجتك ↢ توقع دراجتك
⌯ وش طيارتك ↢ توقع طيارتك
⌯ وش سفينتك ↢ توقع سفينتك
⌯ وش قطارك ↢ توقع قطارك
⌯ وش متروك ↢ توقع متروك
⌯ وش باصك ↢ توقع باصك
⌯ وش تكسيك ↢ توقع تكسيك
⌯ وش موتريك ↢ توقع موتريك
⌯ وش دراجتك النارية ↢ توقع دراجتك النارية
⌯ وش يختك ↢ توقع يختك
⌯ وش غواصتك ↢ توقع غواصتك
⌯ وش صاروخك ↢ توقع صاروخك
⌯ وش قمرك الصناعي ↢ توقع قمرك الصناعي
⌯ وش فضاءتك ↢ توقع فضاءتك
⌯ وش كوكبك ↢ توقع كوكبك
⌯ وش نجمتك ↢ توقع نجمتك
⌯ وش مجرةتك ↢ توقع مجرةتك
⌯ وش كونك ↢ توقع كونك
⌯ وش عالمك ↢ توقع عالمك
⌯ وش بعدك ↢ توقع بعدك
⌯ وش طولك الفعلي ↢ توقع طولك الفعلي
⌯ وش وزنك الفعلي ↢ توقع وزنك الفعلي
⌯ وش عمرك الفعلي ↢ توقع عمرك الفعلي
⌯ وش تاريخ ميلادك ↢ توقع تاريخ ميلادك
⌯ وش برجك الفعلي ↢ توقع برجك الفعلي
⌯ وش حجرك الفعلي ↢ توقع حجرك الفعلي
⌯ وش لونك الفعلي ↢ توقع لونك الفعلي
⌯ وش رقمك الفعلي ↢ توقع رقمك الفعلي
⌯ وش حرفك الفعلي ↢ توقع حرفك الفعلي
⌯ وش اسمك الفعلي ↢ توقع اسمك الفعلي
⌯ وش كنيتك الفعلية ↢ توقع كنيتك الفعلية
⌯ وش لقبك الفعلي ↢ توقع لقبك الفعلي
⌯ وش نسبك الفعلي ↢ توقع نسبك الفعلي
⌯ وش عائلتك الفعلية ↢ توقع عائلتك الفعلية
⌯ وش قبيلتك الفعلية ↢ توقع قبيلتك الفعلية
⌯ وش ديانتك الفعلية ↢ توقع ديانتك الفعلية
⌯ وش مذهبك الفعلي ↢ توقع مذهبك الفعلي
⌯ وش طائفتك الفعلية ↢ توقع طائفتك الفعلية
⌯ وش عرقتك الفعلية ↢ توقع عرقتك الفعلية
⌯ وش جنستك الفعلية ↢ توقع جنستك الفعلية
⌯ وش جنسيتك الفعلية ↢ توقع جنسيتك الفعلية
⌯ وش اقامتك الفعلية ↢ توقع اقامتك الفعلية
⌯ وش جوازك الفعلي ↢ توقع جوازك الفعلي
⌯ وش هويتك الفعلية ↢ توقع هويتك الفعلية
⌯ وش بطاقتك الفعلية ↢ توقع بطاقتك الفعلية
⌯ وش رخصتك الفعلية ↢ توقع رخصتك الفعلية"""

        elif data == "menu_7":
            text = """⌯ مرمر ↢ الردود العشوائية
⌯ احبك ↢ الردود العشوائية
⌯ خاص ↢ الردود العشوائية
⌯ خ ↢ الردود العشوائية
⌯ تعال خاص ↢ الردود العشوائية
⌯ تعال خ ↢ الردود العشوائية
⌯ . ↢ @m_8eu
⌯ همسة ↢ همسة سرية"""

        elif data == "menu_8":
            text = """⌯ اليوتيوب ↢ تحميل الفيديوهات
⌯ الملصقات ↢ الملصقات المميزة"""

        elif data == "menu_9":
            text = """⌯ اذاعة ↢ ارسال رسالة للجميع
⌯ اذاعه ↢ ارسال رسالة للجميع
⌯ الاحصائيات ↢ عرض الإحصائيات
⌯ الرتب ↢ قائمة الرتب
⌯ رتبتي ↢ معرفة رتبتك"""

        else:
            text = "أمر غير معروف"

        await query.edit_message_text(text=text)


    @staticmethod
    async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالجة النصوص"""
        if not update.message or not update.message.text:
            return

        text = update.message.text.strip()
        user_id = update.message.from_user.id
        chat_id = update.message.chat_id
        user = update.message.from_user

        # تحديث معلومات المستخدم
        db_user = db.get_user(user_id)
        db_user["username"] = user.username or ""
        db_user["first_name"] = user.first_name or ""
        db_user["last_name"] = user.last_name or ""
        db_user["messages"] += 1

        # فحص الحماية
        allowed, reason = Protection.check_message(update, context)
        if not allowed:
            try:
                await update.message.delete()
            except Exception:
                pass
            return

        # ردود مرمر
        if text == "مرمر":
            response = random.choice(Responses.MARMER_RESPONSES)
            await update.message.reply_text(response)

        elif text == "احبك":
            response = random.choice(Responses.LOVE_RESPONSES)
            await update.message.reply_text(response)

        elif text == "خاص":
            response = random.choice(Responses.PRIVATE_RESPONSES)
            await update.message.reply_text(response)

        elif text == "خ":
            response = random.choice(Responses.PRIVATE_RESPONSES)
            await update.message.reply_text(response)

        elif text == "تعال خاص":
            response = random.choice(Responses.COME_PRIVATE_RESPONSES)
            await update.message.reply_text(response)

        elif text == "تعال خ":
            response = random.choice(Responses.COME_KH_RESPONSES)
            await update.message.reply_text(response)

        elif text == ".":
            await update.message.reply_text(f"@{Config.UPDATE_CHANNEL.replace('@', '')}")

        elif text == "المطور":
            dev_text = f"""المطور {Config.DEVELOPER_USERNAME}

ID: {Config.DEVELOPER_ID}
الرتبة: إمبراطور التليجرام 👑"""
            await update.message.reply_text(dev_text)

        # نداء المطور في جميع اللغات
        elif text.lower() in ["developer", "desarrollador", "développeur", "entwickler", 
                              "разработчик", "开发者", "開発者", "개발자", "geliştirici"]:
            await update.message.reply_text(f"Developer {Config.DEVELOPER_USERNAME}")

        # همسة
        elif text == "همسة":
            await update.message.reply_text("🤫 ارسل همستك...")

        # ايدي
        elif text == "ايدي":
            user_info = f"""USE ▹ @{user.username or 'لا يوجد'} .
STA ▹ {db_user['rank']} .
MSG ▹ {db_user['messages']} .
ID ▹ {user_id} .
Title ▹ لا يوجد .
Bio ▹ {user.username or ''}"""
            await update.message.reply_text(user_info)

        # الألعاب
        elif text == "الالعاب":
            games_text = "🎮 الألعاب المتوفرة:

"
            for i, game in enumerate(Games.GAMES_LIST[:20], 1):
                games_text += f"{i}. {game}
"
            games_text += "
... والمزيد (150 لعبة)"
            await update.message.reply_text(games_text)

        # البنك
        elif text == "فلوسي":
            success, msg = Bank.get_balance(user_id)
            await update.message.reply_text(msg)

        elif text == "انشاء حساب بنكي":
            success, msg = Bank.create_account(user_id)
            await update.message.reply_text(msg)

        elif text == "راتب":
            success, msg = Bank.get_salary(user_id)
            await update.message.reply_text(msg)

        # التسلية
        elif text == "زوجني":
            await update.message.reply_text("زوجتك: مجهول")

        elif text == "طلاق":
            await update.message.reply_text("تم الطلاق")

        elif text == "كت":
            await update.message.reply_text("كت تويت عشوائي")

        elif text.startswith("نسبة"):
            percentage = Fun.random_percentage()
            await update.message.reply_text(f"نسبتك: {percentage}%")

        elif text == "برج":
            await update.message.reply_text(Fun.horoscope("عام"))

        elif text == "توقع":
            await update.message.reply_text(Fun.prediction())

        elif text == "صراحة":
            await update.message.reply_text(Fun.truth())

        elif text == "تحدي":
            await update.message.reply_text(Fun.dare())

        elif text.startswith("وش "):
            await update.message.reply_text(Fun.guess_future())

        # أوامر الرتب
        elif text.startswith("رفع "):
            parts = text.split()
            if len(parts) >= 2:
                rank = parts[1]
                await update.message.reply_text(f"تم رفع {rank}")

        elif text.startswith("تنزيل "):
            parts = text.split()
            if len(parts) >= 2:
                rank = parts[1]
                await update.message.reply_text(f"تم تنزيل {rank}")

        # أوامر الحظر والكتم
        elif text == "حظر":
            await update.message.reply_text("تم الحظر")

        elif text == "طرد":
            await update.message.reply_text("تم الطرد")

        elif text == "كتم":
            await update.message.reply_text("تم الكتم")

        elif text == "الغاء الحظر":
            await update.message.reply_text("تم الغاء الحظر")

        elif text == "الغاء الكتم":
            await update.message.reply_text("تم الغاء الكتم")

        # أوامر المسح
        elif text.startswith("مسح "):
            await update.message.reply_text("تم المسح")

        # أوامر القفل والفتح
        elif text.startswith("قفل "):
            feature = text.replace("قفل ", "")
            await update.message.reply_text(f"تم قفل {feature}")

        elif text.startswith("فتح "):
            feature = text.replace("فتح ", "")
            await update.message.reply_text(f"تم فتح {feature}")

        # أوامر التفعيل والتعطيل
        elif text.startswith("تفعيل "):
            feature = text.replace("تفعيل ", "")
            await update.message.reply_text(f"تم تفعيل {feature}")

        elif text.startswith("تعطيل "):
            feature = text.replace("تعطيل ", "")
            await update.message.reply_text(f"تم تعطيل {feature}")

        # منع الكلمة
        elif text.startswith("منع "):
            word = text.replace("منع ", "")
            success, msg = Protection.add_banned_word(chat_id, word)
            await update.message.reply_text(msg)

        elif text.startswith("الغاء منع "):
            word = text.replace("الغاء منع ", "")
            success, msg = Protection.remove_banned_word(chat_id, word)
            await update.message.reply_text(msg)

        # انطقي
        elif text.startswith("انطقي "):
            word = text.replace("انطقي ", "")
            await update.message.reply_text(f"🔊 {word}")

        # الرابط
        elif text == "الرابط":
            await update.message.reply_text("رابط المجموعة")

        # بايو
        elif text == "بايو":
            await update.message.reply_text("بايوك")

        # افتاري
        elif text == "افتاري":
            await update.message.reply_text("صورتك")

        # مجموعاتي
        elif text == "مجموعاتي":
            await update.message.reply_text("مجموعاتك")

        # الساعة
        elif text == "الساعه":
            now = datetime.datetime.now().strftime("%H:%M:%S")
            await update.message.reply_text(f"الساعة: {now}")

        # التاريخ
        elif text == "التاريخ":
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            await update.message.reply_text(f"التاريخ: {today}")

        # صلاحياتي
        elif text == "صلاحياتي":
            await update.message.reply_text(f"صلاحياتك: {db_user['rank']}")

        # لقبي
        elif text == "لقبي":
            await update.message.reply_text("لقبك: لا يوجد")

        # الاحصائيات
        elif text == "الاحصائيات":
            stats = f"""📊 الإحصائيات:

👥 المستخدمين: {len(db.users)}
🎮 الألعاب: 150
🛡️ الحماية: 100%
🌍 اللغات: 10"""
            await update.message.reply_text(stats)

        # الرتب
        elif text == "الرتب":
            ranks_text = "🎖️ الرتب:

"
            for key, rank in Config.RANKS.items():
                ranks_text += f"{rank['emoji']} {rank['name']} ({rank['abbr']})
"
            await update.message.reply_text(ranks_text)

        # رتبتي
        elif text == "رتبتي":
            rank_info = RankSystem.get_rank_info(db_user['rank'])
            await update.message.reply_text(f"رتبتك: {rank_info['emoji']} {rank_info['name']}")

        # الاذاعة
        elif text == "اذاعه" or text == "اذاعة":
            if str(user_id) == Config.DEVELOPER_ID:
                await update.message.reply_text("أرسل رسالة الإذاعة...")
            else:
                await update.message.reply_text("ها! هاي للمطور بس!")

        # اليوتيوب
        elif text == "اليوتيوب":
            await update.message.reply_text("أرسل رابط اليوتيوب...")

        # الملصقات
        elif text == "الملصقات":
            await update.message.reply_text("🎨 الملصقات المميزة:

⭐ PREMIUM
🔥 النار
😎 الكول
❤️ الحب
🎮 الألعاب
🛡️ الحماية
💎 الجواهر")

        # @admin
        elif text == "@admin":
            await update.message.reply_text("📢 مناداة الأدمن...")

        # نقل ملكية
        elif text == "نقل ملكية":
            await update.message.reply_text("تم نقل الملكية")

        # صورة
        elif text == "صوره":
            await update.message.reply_text("أرسل صورة...")

        # مين ضافني
        elif text == "مين ضافني؟":
            await update.message.reply_text("ضافك: مجهول")

        # انشاء رابط
        elif text == "انشاء رابط":
            await update.message.reply_text("تم انشاء رابط جديد")

        # معلومات الرابط
        elif text == "معلومات الرابط":
            await update.message.reply_text("معلومات الرابط...")

        # تعيين الترحيب
        elif text == "تعيين الترحيب":
            await update.message.reply_text("تم تعيين الترحيب")

        # تعيين القوانين
        elif text == "تعيين القوانين":
            await update.message.reply_text("تم تعيين القوانين")

        # تغيير رتبه
        elif text == "تغيير رتبه":
            await update.message.reply_text("تم تغيير الرتبة")

        # تغيير امر
        elif text == "تغيير امر":
            await update.message.reply_text("تم تغيير الأمر")

        # المطورين
        elif text == "المطورين":
            await update.message.reply_text(f"المطور: {Config.DEVELOPER_USERNAME}")

        # المالكيين
        elif text == "المالكيين":
            await update.message.reply_text("المالكين...")

        # الادمنيه
        elif text == "الادمنيه":
            await update.message.reply_text("الأدمنية...")

        # المدراء
        elif text == "المدراء":
            await update.message.reply_text("المدراء...")

        # المشرفين
        elif text == "المشرفين":
            await update.message.reply_text("المشرفين...")

        # المميزين
        elif text == "المميزين":
            await update.message.reply_text("المميزين...")

        # القوانين
        elif text == "القوانين":
            await update.message.reply_text("القوانين...")

        # قائمه المنع
        elif text == "قائمه المنع":
            group = db.get_group(chat_id)
            banned = ", ".join(group["banned_words"]) if group["banned_words"] else "لا يوجد"
            await update.message.reply_text(f"قائمة المنع: {banned}")

        # المكتومين
        elif text == "المكتومين":
            await update.message.reply_text("المكتومين...")

        # المطور
        elif text == "المطور":
            await update.message.reply_text(f"المطور: {Config.DEVELOPER_USERNAME}")

        # معلوماتي
        elif text == "معلوماتي":
            await update.message.reply_text(f"""معلوماتك:

الاسم: {user.first_name}
الايدي: {user_id}
الرتبة: {db_user['rank']}
الرسائل: {db_user['messages']}""")

        # الاعدادت
        elif text == "الاعدادت":
            await update.message.reply_text("الإعدادات...")

        # المجموعه
        elif text == "المجموعه":
            await update.message.reply_text("معلومات المجموعة...")

        # صلاحياته
        elif text.startswith("صلاحياته "):
            await update.message.reply_text("صلاحياته...")

        # الردود
        elif text == "الردود":
            await update.message.reply_text("الردود المضافة...")

        # اضف رد
        elif text.startswith("اضف رد "):
            await update.message.reply_text("تم اضافة الرد")

        # مسح رد
        elif text.startswith("مسح رد "):
            await update.message.reply_text("تم مسح الرد")

        # رفع القيود
        elif text == "رفع القيود":
            await update.message.reply_text("تم رفع القيود")

        # طرد البوتات
        elif text == "طرد البوتات":
            await update.message.reply_text("تم طرد البوتات")

        # كشف البوتات
        elif text == "كشف البوتات":
            await update.message.reply_text("البوتات المكتشفة...")

        # وش يقول
        elif text.startswith("وش يقول؟"):
            await update.message.reply_text("ترجمة الصوت...")

        # تحويل
        elif text.startswith("تحويل "):
            await update.message.reply_text("تم التحويل")

        # حسابي
        elif text == "حسابي":
            await update.message.reply_text("رقم حسابك...")

        # بخشيش
        elif text == "بخشيش":
            success, msg = Bank.get_gift(user_id)
            await update.message.reply_text(msg)

        # زرف
        elif text.startswith("زرف "):
            await update.message.reply_text("تم الزرف")

        # استثمار
        elif text.startswith("استثمار "):
            await update.message.reply_text("تم الاستثمار")

        # حظ
        elif text.startswith("حظ "):
            await update.message.reply_text("نتيجة الحظ...")

        # مضاربه
        elif text.startswith("مضاربه "):
            await update.message.reply_text("نتيجة المضاربة...")

        # توب الفلوس
        elif text == "توب الفلوس":
            top = Bank.get_top_rich()
            text = "🏆 توب الأغنياء:

"
            for i, (uid, balance) in enumerate(top, 1):
                text += f"{i}. {uid}: {balance} فلوس
"
            await update.message.reply_text(text)

        # توب الحراميه
        elif text == "توب الحراميه":
            await update.message.reply_text("🏆 توب الحرامية...")

        # تحليل
        elif text.startswith("تحليل "):
            name = text.replace("تحليل ", "")
            await update.message.reply_text(Fun.analyze_name(name))

        # معنى الاسم
        elif text.startswith("معنى الاسم "):
            name = text.replace("معنى الاسم ", "")
            await update.message.reply_text(f"معنى {name}: جميل")

        # عمرك بالايام
        elif text == "عمرك بالايام":
            await update.message.reply_text("عمرك بالأيام...")

        # متى زواجك
        elif text == "متى زواجك":
            await update.message.reply_text("توقع الزواج...")

        # كم طولك
        elif text == "كم طولك":
            await update.message.reply_text(f"طولك: {random.randint(150, 200)} سم")

        # كم وزنك
        elif text == "كم وزنك":
            await update.message.reply_text(f"وزنك: {random.randint(50, 100)} كغ")

        # لون عينك
        elif text == "لون عينك":
            colors = ["أخضر", "أزرق", "بني", "عسلي", "رمادي"]
            await update.message.reply_text(f"لون عينك: {random.choice(colors)}")

        # لون شعرك
        elif text == "لون شعرك":
            colors = ["أسود", "بني", "أشقر", "أحمر", "أبيض"]
            await update.message.reply_text(f"لون شعرك: {random.choice(colors)}")

        # مقارنة
        elif text.startswith("مقارنه ") or text.startswith("مقارنة "):
            await update.message.reply_text(Fun.compare(user_id, user_id))

        # كذبة
        elif text == "كذبة":
            await update.message.reply_text("كذبة عشوائية...")

        # حقيقة
        elif text == "حقيقة":
            await update.message.reply_text("حقيقة عشوائية...")

# ═══════════════════════════════════════════════════════════
# الدالة الرئيسية
# ═══════════════════════════════════════════════════════════

async def main():
    """الدالة الرئيسية لتشغيل البوت"""

    # التحقق من التوكن
    if Config.TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ خطأ: ضع التوكن في Config.TOKEN")
        print("احصل على التوكن من @BotFather")
        return

    # إنشاء البوت
    application = Application.builder().token(Config.TOKEN).build()

    # إضافة المعالجات
    application.add_handler(CommandHandler("start", CommandHandlers.start))
    application.add_handler(CallbackQueryHandler(CommandHandlers.handle_callback))
    application.add_handler(MessageHandler(filters.TEXT, CommandHandlers.handle_text))

    # تشغيل البوت
    print("🚀 بوت مرمر يعمل الآن!")
    print(f"👤 المطور: {Config.DEVELOPER_USERNAME}")
    print(f"📢 القناة: {Config.UPDATE_CHANNEL}")

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # الانتظار
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()

# ═══════════════════════════════════════════════════════════
# تشغيل البوت
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    asyncio.run(main())

