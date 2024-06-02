from dataclasses import dataclass


@dataclass
class MainKB:
    main_menu = ['Вернуться в основное меню', 'main_menu']
    info_function = ['Получить информацию о возможностях бота', 'info_function']    # general
    registration_bot = ['Зарегистрироваться в боте', 'registration_bot']    # general
    registration_tournament = ['Зарегистрироваться в турнире', 'registration_tournament']    # general
    cancel = ['Выйти', 'cancel']    # general
    back = ['Назад', 'back']    # general


@dataclass
class RegistrationBotKB:
    your_name = ['Ваше имя', 'your_name']
    your_surname = ['Ваша фамилия', 'your_surname']
    your_phone = ['Ваш телефон', 'your_phone']
    your_handicap = ['Ваш handicap', 'your_handicap']
    confirm = ['Подтвердить регистрацию в боте', 'confirm_registration_bot']


@dataclass
class RegistrationTournamentKB:
    confirm = ['Подтвердить регистрацию в турнире', 'confirm_registration_tournament']


@dataclass
class GameKB:
    start_game = ['Запустить игру', 'start_game']
    list_available_tournament = ['Список доступных турниров', 'list_available_tournament']
    completed_game = ['Завершить игру', 'completed_game']
    back_to_game = ['Вернуться к игре', 'back_to_game']
    top = ['Рейтинг', 'top']


@dataclass
class AdminKB:
    login = ['Войти', 'confirm']
    backspace = ['Удалить символ', 'backspace']
    save = ['Сохранить изменения', 'save']
    confirm = ['Подтвердить', 'confirm']
    # region Tournaments
    tournaments = ['Турниры', 'tournaments']
    top_tournament = ['Рейтинг турнира', 'top_tournament']
    create_tournaments = ['Создать турнир', 'create_tournaments']
    update_tournaments = ['Обновить турнир', 'update_tournaments']
    entered_name = ['Ввести название турнира', 'entered_name']
    entered_type = ['Выбрать тип турнира', 'entered_type']
    entered_flights = ['Ввести максимальное количество флайтов', 'entered_flights']
    entered_course_name = ['Выбрать поле', 'entered_course_name']
    entered_start = ['Ввести дату старта', 'entered_start']
    entered_end = ['Ввести дату конца', 'entered_end']
    entered_hcp = ['Ввести HCP', 'entered_hcp']
    start_tournaments = ['Запустить турнир', 'start_tournaments']
    delete_tournaments = ['Удалить турнир', 'delete_tournaments']
    nearest_tournaments = ['Ближайшие за 30 дней турниры', 'nearest_tournaments']
    all_tournaments = ['Все турниры', 'all_tournaments']
    # endregion Tournaments
    # region Users
    users = ['Пользователи', 'users']
    update_handicap = ['Изменить гандикап', 'update_handicap']
    delete_user = ['Удалить пользователя', 'delete_user']
    # endregion Users
    # region Admins
    admins = ['Админы', 'admins']
    delete_admin = ['Удалить админа', 'delete_admin']
    entered_login = ['Добавить логин', 'entered_login']
    entered_password = ['Добавить пароль', 'entered_password']
    admin_registration = ['Зарегистрировать админа', 'admin_registration']
    confirm_registration = ['Подтвердить регистрацию', 'confirm_registration']
    # endregion Admins
    # region Courses
    courses = ['Гольф-поля', 'course']
    create_course = ['Создать гольф-поле', 'create_course']
    create_hole = ['Создать лунку', 'create_hole']
    edit_holes = ['Редактировать лунки', 'edit_holes']
    delete_holes = ['Удалить лунки', 'delete_holes']
    delete_course = ['Удалить гольф-поле', 'delete_course']
    number_hole = ['Номер лунки', 'number_hole']
    par_hole = ['Пар лунки', 'par_hole']
    difficulty_hole = ['Сложность лунки', 'difficulty_hole']
    # endregion Courses
    close_admin_panel = ['Закрыть админ панель', 'close_admin_panel']
    main_admin_panel = ['Основное меню админ панели', 'main_admin_panel']
