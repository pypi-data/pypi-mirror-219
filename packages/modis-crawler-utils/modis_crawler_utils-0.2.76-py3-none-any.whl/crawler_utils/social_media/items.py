import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List

from dateparser import parse

UnixTimestamp = int  # Имитация типа timestamp


def class_output(obj_class: object):
    # Метод, не пропускающий в конечный JSON-файл пустые поля.
    # Необходимо использовать для каждого поля, имеющего пользовательский тип
    previous_list_of_fields = dir(obj_class)
    current_list_of_fields = list()
    for field in previous_list_of_fields:
        if "__" not in field:
            current_list_of_fields.append(field)
    current_dict = dict()
    for field in current_list_of_fields:
        if getattr(obj_class, field):
            current_dict[field] = getattr(obj_class, field)
    return current_dict


def list_of_types_output(
        list_of_objects: List[object]):  # Метод для фильтрации на пустые поля списков объектов
    dict_of_obj = list()
    for obj in list_of_objects:
        dict_of_obj.append(class_output(obj))
    return dict_of_obj


def parse_birth_date_to_class(date_text):
    # Дату рождения нельзя разбирать с помощью dateparser потому, что для
    # корректной работы он требует либо чтобы получаемая им дата всегда была полной(год.месяц.день),
    # либо указать некие стандартные значения, которые будут использоваться вместо неполученных
    # частей даты
    date_text = str(date_text).strip()
    data_formats = {"%B %d %Y", "%b %d %Y", "%d %B %Y", "%d %b %Y", "%B %d", "%b %d", "%d %B",
                    "%d %b", "%B %Y", "%b %Y", "%Y %B", "%Y %b", "%Y"}
    for data_format in data_formats:
        try:
            dt = datetime.strptime(date_text.split(' (')[0], data_format)
            if data_format.count('%') == 3:
                return BirthDay(day=dt.day, month=dt.month, year=dt.year)
            if data_format.count('%') == 2 and "d" in data_format.lower():
                return BirthDay(day=dt.day, month=dt.month)
            if data_format.count('%') == 2 and "y" in data_format.lower():
                return BirthDay(month=dt.month, year=dt.year)
            if data_format.count('%') == 1:
                return BirthDay(year=dt.year)
        except ValueError:
            continue


def parse_date(date_text):
    if date_text is None:
        return None
    dt = parse(date_text.rstrip())
    return int(time.mktime(dt.timetuple()))


class AccountStatus(Enum):
    ACTIVE = "Active"
    DELETED = "Deleted"
    BANNED = "Banned"
    CLOSED = "Closed"
    NOT_SPECIFIED = None


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    NOT_SPECIFIED = None


class NameType(Enum):
    MAIDEN_NAME = "Maiden Name"
    NICKNAME = "Nickname"
    NOT_SPECIFIED = None


class EducationalInstitutionType(Enum):
    SCHOOL = "School"
    COLLEGE = "College"
    INSTITUTE = "Institute"
    UNIVERSITY = "University"
    ACADEMY = "Academy"
    COURSES = "Courses"
    NOT_SPECIFIED = None


class EducationStatus(Enum):
    PUPIL = "Pupil"
    STUDENT = "Student"
    GRADUATE = "Graduate"
    NOT_SPECIFIED = None


class MessageType(Enum):
    POST = "Post"
    COMMENT = "Comment"
    VIDEO = "Video"
    PHOTO = "Photo"
    AUDIO = "Audio"
    NOT_SPECIFIED = None


class AccessType(Enum):
    PUBLIC = "Public"
    CLOSED = "Closed"
    NOT_SPECIFIED = None


class RelationshipStatus(Enum):
    NOT_MARRIED = "Not married"
    DATING = "Dating"
    ENGAGED = "Engaged"
    MARRIED = "Married"
    IN_A_CIVIL_MARRIAGE = "In a civil marriage"
    IN_LOVE = "In love"
    ITS_DIFFICULT = "It's difficult"
    IN_ACTIVE_SEARCH = "In active search"
    SEPARATED = "Separated"
    IN_A_FREE_RELATIONSHIP = "In a free relationship"
    IN_A_HOME_PARTNERSHIP = "In a home partnership"
    WIDOWED = "Widowed"
    NOT_SPECIFIED = None


class FriendsOrFollowers(Enum):
    # В ОК бывают Либо друзья Либо подписчики, в то время, как в модели есть и поле
    # followers и поле friends , поэтому при выставлении этих полей необходимо определить
    # какое поле используется на ресурсе
    FOLLOWERS = "Subscribers"
    FRIENDS = "Friends"


@dataclass
class BirthDay:
    day: int = None
    month: int = None
    year: int = None


@dataclass
class Date:
    day: int = None
    month: int = None
    year: int = None
    hour: int = None
    minutes: int = None


@dataclass
class Location:
    raw: str = None
    city: str = None
    country: str = None
    latitude: float = None  # Вместо double
    longitude: float = None  # Вместо double
    street: str = None
    postal_code: str = None
    country_code: str = None
    # ____________Other Fields_________
    url: str = None


@dataclass
class OtherName:
    name: str
    other_name_type: NameType = None


@dataclass
class EducationalInstitution:
    name: str
    edu_id: str = None
    education_institution_type: EducationalInstitutionType = None
    from_date: Date = None
    until_date: Date = None
    city: str = None
    country: str = None
    status: EducationStatus = None
    faculty: str = None
    chair: str = None
    speciality: str = None
    # __________Other Fields____________
    url: str = None  # FB
    description: str = None  # FB

    def __post_init__(self):
        # Этот метод запускается автоматически после инициализации класса, в нём происходит
        # пост-обработка полей класса. В данном случае мы меняем тип поля на словарь или список
        # словарей (поскольку в JSON поля уходят именно в виде словарей и списков) и с помощью
        # методов class_output и list_of_types_output получаем словарь или список словарей уже
        # без пустых полей
        if self.from_date:
            self.from_date: dict = class_output(self.from_date)
        if self.until_date:
            self.until_date: dict = class_output(self.until_date)


@dataclass
class RelativesAndMaritalStatus:
    name: str
    relatives_and_marital_status_type: str = None
    relative_id: str = None
    url: str = None


@dataclass
class Workplace:
    name: str
    career_id: str = None
    from_date: Date = None
    until_date: Date = None
    city: str = None
    country: str = None
    position: str = None
    # __________Other Fields____________
    url: str = None  # FB
    description: str = None  # FB
    location: Location = None  # FB

    def __post_init__(self):
        # Этот метод запускается автоматически после инициализации класса, в нём происходит
        # пост-обработка полей класса. В данном случае мы меняем тип поля на словарь или список
        # словарей (поскольку в JSON поля уходят именно в виде словарей и списков) и с помощью
        # методов class_output и list_of_types_output получаем словарь или список словарей уже
        # без пустых полей
        if self.from_date:
            self.from_date: dict = class_output(self.from_date)
        if self.until_date:
            self.until_date: dict = class_output(self.until_date)
        if self.location:
            self.location: dict = class_output(self.location)


@dataclass
class MilitaryUnit:
    unit: str
    unit_id: str = None
    from_date: Date = None
    until_date: Date = None

    def __post_init__(self):
        # Этот метод запускается автоматически после инициализации класса, в нём происходит
        # пост-обработка полей класса. В данном случае мы меняем тип поля на словарь или список
        # словарей (поскольку в JSON поля уходят именно в виде словарей и списков) и с помощью
        # методов class_output и list_of_types_output получаем словарь или список словарей уже
        # без пустых полей
        if self.from_date:
            self.from_date: dict = class_output(self.from_date)
        if self.until_date:
            self.until_date: dict = class_output(self.until_date)


@dataclass
class VolunteerExperience:
    name: str = None
    position: str = None
    description: str = None
    from_date: Date = None
    until_date: Date = None

    def __post_init__(self):
        # Этот метод запускается автоматически после инициализации класса, в нём происходит
        # пост-обработка полей класса. В данном случае мы меняем тип поля на словарь или список
        # словарей (поскольку в JSON поля уходят именно в виде словарей и списков) и с помощью
        # методов class_output и list_of_types_output получаем словарь или список словарей уже
        # без пустых полей
        if self.from_date:
            self.from_date: dict = class_output(self.from_date)
        if self.until_date:
            self.until_date: dict = class_output(self.until_date)


@dataclass
class Projects:
    title: str = None
    url: str = None
    from_date: Date = None
    until_date: Date = None

    def __post_init__(self):
        # Этот метод запускается автоматически после инициализации класса, в нём происходит
        # пост-обработка полей класса. В данном случае мы меняем тип поля на словарь или список
        # словарей (поскольку в JSON поля уходят именно в виде словарей и списков) и с помощью
        # методов class_output и list_of_types_output получаем словарь или список словарей уже
        # без пустых полей
        if self.from_date:
            self.from_date: dict = class_output(self.from_date)
        if self.until_date:
            self.until_date: dict = class_output(self.until_date)


@dataclass
class Certificate:
    name: str = None
    url: str = None
    company_url: str = None
    authority: str = None
    from_date: Date = None
    until_date: Date = None

    def __post_init__(self):
        # Этот метод запускается автоматически после инициализации класса, в нём происходит
        # пост-обработка полей класса. В данном случае мы меняем тип поля на словарь или список
        # словарей (поскольку в JSON поля уходят именно в виде словарей и списков) и с помощью
        # методов class_output и list_of_types_output получаем словарь или список словарей уже
        # без пустых полей
        if self.from_date:
            self.from_date: dict = class_output(self.from_date)
        if self.until_date:
            self.until_date: dict = class_output(self.until_date)


@dataclass
class Contact:
    value: str
    contact_type: str


@dataclass
class Attachment:
    url: str
    attachment_type: str = None
    title: str = None
    path: str = None
    filename: str = None
    checksum: str = None
    status: str = None
    # __________Other Fields____________
    attachment_id: str = None  # VK
    owner_id: str = None  # VK
    image_url: str = None  # VK
    duration: float = None  # VK
    artist: str = None  # VK


@dataclass
class SocialConnection:
    _url: str
    platform: str
    from_id: str
    to_id: str
    social_connection_type: str
    type: str = field(default='social_connection', init=False)
    # __________Other Fields____________
    from_url: str = None  # FB
    to_url: str = None  # FB
    relation_type: str = None  # FB
    role: str = None  # FB
    liked_type: str = None  # FB
    like_type: str = None  # FB
    _timestamp: UnixTimestamp = int(time.time())
    _attachments: List["Attachment"] = None

    def __post_init__(self):
        # Этот метод запускается автоматически после инициализации класса, в нём происходит
        # пост-обработка полей класса. В данном случае мы меняем тип поля на словарь или список
        # словарей (поскольку в JSON поля уходят именно в виде словарей и списков) и с помощью
        # методов class_output и list_of_types_output получаем словарь или список словарей уже
        # без пустых полей
        if self._attachments:
            self._attachments: List[dict] = list_of_types_output(self._attachments)


@dataclass
class Company:
    _url: str = None
    name: str = None
    platform: str = None
    company_id: int = None
    type: str = field(default='company_profile', init=False)
    # ______________Main Info__________________
    is_snippet: bool = False
    main_photo: str = None
    location: Location = None
    contact_info: str = None
    start_date: Date = None
    # __________Other Fields____________
    description: str = None
    members_count: int = None
    category: List[str] = None
    _timestamp: UnixTimestamp = int(time.time())
    _attachments: List[Attachment] = None

    def __post_init__(self):
        # Этот метод запускается автоматически после инициализации класса, в нём происходит
        # пост-обработка полей класса. В данном случае мы меняем тип поля на словарь или список
        # словарей (поскольку в JSON поля уходят именно в виде словарей и списков) и с помощью
        # методов class_output и list_of_types_output получаем словарь или список словарей уже
        # без пустых полей
        if self.start_date:
            self.start_date: dict = class_output(self.start_date)
        if self.location:
            self.location: dict = class_output(self.location)
        if self._attachments:
            self._attachments: List[dict] = list_of_types_output(self._attachments)


@dataclass
class HistoryMessage:
    _url: str
    platform: str
    message_id: str
    text: str
    date: UnixTimestamp
    type: str = field(default='message', init=False)
    owner_id: str = None
    message_type: MessageType = None
    author: List["MessageAuthor"] = None
    title: str = None
    subtitle: str = None
    replies_to: str = None
    replies_count: int = None
    reactions_count: int = None
    views_count: int = None
    location: Location = None
    category: str = None
    tags: List[str] = None
    hashtags: List[str] = None
    agency: str = None
    # __________Other Fields____________
    is_shared: bool = False  # OK
    shared_in: str = None  # OK
    image_caption: str = None  # Instagram
    is_pinned: bool = False  # VK
    replies_to_user: str = None  # VK
    scope: str = None  # FB
    author_url: str = None  # FB
    quotes_count: int = None  # Twitter
    retweet_count: int = None  # Twitter
    story_url: str = None  # yandex_news
    description: str = None  # TASS
    datetime_modified: UnixTimestamp = None  # RIA, Vedomosti
    _timestamp: UnixTimestamp = int(time.time())
    _attachments: List["Attachment"] = None

    def __post_init__(self):
        # Этот метод запускается автоматически после инициализации класса, в нём происходит
        # пост-обработка полей класса. В данном случае мы меняем тип поля на словарь или список
        # словарей (поскольку в JSON поля уходят именно в виде словарей и списков) и с помощью
        # методов class_output и list_of_types_output получаем словарь или список словарей уже
        # без пустых полей
        if self.message_type:
            if isinstance(self.message_type, MessageType) and self.message_type != MessageType.NOT_SPECIFIED:
                self.type = self.message_type.value.lower()
            elif isinstance(self.message_type, str):
                self.type = self.message_type.lower()
        if self.author:
            self.author: List[dict] = list_of_types_output(self.author)
        if self.location:
            self.location: dict = class_output(self.location)
        if self._attachments:
            self._attachments: List[dict] = list_of_types_output(self._attachments)


@dataclass
class Message(HistoryMessage):
    copy_history: List[HistoryMessage] = None


@dataclass
class MessageAuthor:
    name: str
    id: str = None


@dataclass
class UserProfile:
    _url: str
    platform: str
    user_id: str
    name: str
    type: str = field(default='user_profile', init=False)
    account_status: AccountStatus = None
    # ______________Main Info__________________
    is_snippet: bool = False
    full_name: str = None
    first_name: str = None
    last_name: str = None
    middle_name: str = None
    login: str = None
    gender: Gender = None
    current_place: Location = None
    birth_place: Location = None
    places_lived: List[Location] = None
    birth_day: BirthDay = None
    other_names: List[OtherName] = None
    # _______________Relationship_______________
    relation_status: RelationshipStatus = None
    relatives: List[RelativesAndMaritalStatus] = None
    interested_in: Gender = None
    friends_count: int = None
    followers_count: int = None
    # _________________Education_________________
    education: List[EducationalInstitution] = None
    career: List[Workplace] = None
    military: List[MilitaryUnit] = None
    # ____________Religion and Political_________
    religion: str = None
    political: str = None
    # ____________Hobbies and interests___________
    interests: str = None
    music: str = None
    movies: str = None
    tv: str = None
    books: str = None
    games: str = None
    quotes: str = None
    activities: str = None
    sports: str = None
    teams: str = None
    about: str = None
    # __________Other Fields____________
    languages: List[str] = None
    contacts: List[Contact] = None
    main_photo: str = None
    cover_photo: str = None
    created: UnixTimestamp = None  # Вместо ts
    updated: UnixTimestamp = None  # Вместо ts
    last_logged_in: UnixTimestamp = None  # Вместо ts
    verified: bool = None
    status: str = None
    # _________Resource-specific Fields_________
    volunteer_experience: List[VolunteerExperience] = None  # Linkedin
    projects: List[Projects] = None  # Linkedin
    courses: List[str] = None  # Linkedin
    certificates: List[Certificate] = None  # Linkedin
    smoking: str = None  # VK   Возможно нужен будет enum с вариантами
    alcohol: str = None  # VK   Возможно нужен будет enum с вариантами
    values_in_life: str = None  # VK
    values_in_people: str = None  # VK
    inspired_by: str = None  # VK
    skills: List[str] = None  # FB, Linkedin
    _timestamp: UnixTimestamp = int(time.time())
    _attachments: List["Attachment"] = None

    def __post_init__(self):
        # Этот метод запускается автоматически после инициализации класса, в нём происходит
        # пост-обработка полей класса. В данном случае мы меняем тип поля на словарь или список
        # словарей (поскольку в JSON поля уходят именно в виде словарей и списков) и с помощью
        # методов class_output и list_of_types_output получаем словарь или список словарей уже
        # без пустых полей
        if self.current_place:
            self.current_place: dict = class_output(self.current_place)
        if self.birth_place:
            self.birth_place: dict = class_output(self.birth_place)
        if self.birth_day:
            self.birth_day: dict = class_output(self.birth_day)
        if self.places_lived:
            self.places_lived: List[dict] = list_of_types_output(self.places_lived)
        if self.other_names:
            self.other_names: List[dict] = list_of_types_output(self.other_names)
        if self.relatives:
            self.relatives: List[dict] = list_of_types_output(self.relatives)
        if self.education:
            self.education: List[dict] = list_of_types_output(self.education)
        if self.career:
            self.career: List[dict] = list_of_types_output(self.career)
        if self.military:
            self.military: List[dict] = list_of_types_output(self.military)
        if self.contacts:
            self.contacts: List[dict] = list_of_types_output(self.contacts)
        if self.volunteer_experience:
            self.volunteer_experience: List[dict] = list_of_types_output(self.volunteer_experience)
        if self.projects:
            self.projects: List[dict] = list_of_types_output(self.projects)
        if self.certificates:
            self.certificates: List[dict] = list_of_types_output(self.certificates)
        if self._attachments:
            self._attachments: List[dict] = list_of_types_output(self._attachments)


@dataclass
class GroupProfile:
    _url: str
    platform: str
    comm_id: str
    name: str
    type: str = field(default='group_profile', init=False)
    is_snippet: bool = False
    account_status: AccountStatus = None
    description: str = None
    members_count: int = None
    main_photo: str = None
    cover_photo: str = None
    place: Location = None
    start_date: UnixTimestamp = None
    # __________Other Fields____________
    access_type: AccessType = None  # FB
    page_type: str = None  # FB
    categories: List[str] = None  # FB
    contacts: List[Contact] = None  # FB
    other_information: dict = None  # FB
    business_info: dict = None  # FB
    members: List[SocialConnection] = None  # FB
    milestones: dict = None  # FB
    page_story_url: str = None  # FB
    activity_status: dict = None  # FB
    _timestamp: UnixTimestamp = int(time.time())
    _attachments: List["Attachment"] = None

    def __post_init__(self):
        # Этот метод запускается автоматически после инициализации класса, в нём происходит
        # пост-обработка полей класса. В данном случае мы меняем тип поля на словарь или список
        # словарей (поскольку в JSON поля уходят именно в виде словарей и списков) и с помощью
        # методов class_output и list_of_types_output получаем словарь или список словарей уже
        # без пустых полей
        if self.place:
            self.place: dict = class_output(self.place)
        if self.contacts:
            self.contacts: List[dict] = list_of_types_output(self.contacts)
        if self.members:
            self.members: List[dict] = list_of_types_output(self.members)
        if self._attachments:
            self._attachments: List[dict] = list_of_types_output(self._attachments)


def set_friends_or_followers(followers_or_friend_field_text,
                             followers_or_friend_count,
                             friends_or_followers_field: FriendsOrFollowers):
    if followers_or_friend_count and \
            followers_or_friend_field_text == friends_or_followers_field.value:
        return int(followers_or_friend_count.replace(" ", ""))
    else:
        return None


def set_gender(gender):
    if gender is None:
        return Gender.NOT_SPECIFIED.value
    gender = gender.upper()
    if gender == str(Gender.MALE.value).upper():
        return Gender.MALE.value
    if gender == str(Gender.FEMALE.value).upper():
        return Gender.FEMALE.value
    else:
        return Gender.OTHER.value
