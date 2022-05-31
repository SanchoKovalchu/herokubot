import time
from datetime import datetime
from bot_create import connection, cursor, bot


async def send_message():
    sql = "SELECT * FROM add_file_storage"
    cursor.execute(sql)
    raw_dates_string = []
    file_id_array = []
    dates_array_for_comparing = []

    i = -1
    for row in cursor:
        i += 1
        raw_dates_string.append(row["date_time"])
        file_id_array.append(row["file_id"])


    sql = "SELECT * FROM file_storage"
    cursor.execute(sql)
    file_id_storage_array = []
    file_type_storage_array = []
    file_name_storage_array = []
    file_description_storage_array = []
    file_subject_storage_array = []
    file_groups_storage_array = []

    i = -1
    for row in cursor:
        i += 1
        file_id_storage_array.append(row["file_id"])
        file_type_storage_array.append(row["file_type"])
        file_name_storage_array.append(row["file_name"])
        file_description_storage_array.append(row["description"])
        file_subject_storage_array.append(row["subject"])
        file_groups_storage_array.append(row["groups"])


    sql = "SELECT * FROM disciplines"
    cursor.execute(sql)
    sb_full_name_array = []
    cafedra_name_array = []

    i = -1
    for row in cursor:
        i += 1
        sb_full_name_array.append(row["sb_full_name"])
        cafedra_name_array.append(row["cafedra_name"])

    sql = "SELECT * FROM study_program_list"
    cursor.execute(sql)
    sp_abr_name_array = []
    cafedra_name_program_array = []

    i = -1
    for row in cursor:
        i += 1
        sp_abr_name_array.append(row["sp_abr_name"])
        cafedra_name_program_array.append(row["cafedra_name"])


    sql = "SELECT * FROM student_data"
    cursor.execute(sql)
    sp_name_array = []
    user_id_array = []
    user_group_array = []

    i = -1
    for row in cursor:
        i += 1
        sp_name_array.append(row["sp"])
        user_id_array.append(row["user_id"])
        user_group_array.append(row["st_group"])

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    unixtime = datetime.strptime(str(dt_string), '%d-%m-%Y %H:%M:%S')
    unixtime_now = time.mktime(unixtime.timetuple())
    for k in range(len(raw_dates_string)):
        date_string = raw_dates_string[k].split(', ')
        dates_array_for_comparing.append(date_string[0])
        for l in range(len(dates_array_for_comparing)):
            if unixtime_now > float(dates_array_for_comparing[l]):
                for j in range(len(file_id_storage_array)):
                    if file_id_storage_array[j] == file_id_array[k]:
                        send_groups_array = file_groups_storage_array[j].split(', ')
                        for ii in range(len(sb_full_name_array)):
                            if file_subject_storage_array[j] == sb_full_name_array[ii]:
                                for iii in range(len(cafedra_name_program_array)):
                                    if cafedra_name_array[ii] == cafedra_name_program_array[iii]:
                                        for jj in range(len(send_groups_array)):
                                            for iiii in range(len(sp_name_array)):
                                                if str(user_group_array[iiii]) == send_groups_array[jj]:
                                                    if sp_name_array[iiii] == sp_abr_name_array[iii]:
                                                        try:
                                                            message_text = f'Назва: {file_name_storage_array[j]}\nОпис: { file_description_storage_array[j]}'
                                                            match file_type_storage_array[j]:
                                                                case 'photo':
                                                                    await bot.send_photo(user_id_array[iiii], file_id_storage_array[j], caption=message_text)
                                                                case 'video':
                                                                    await bot.send_video(user_id_array[iiii], file_id_storage_array[j], caption=message_text)
                                                                case 'audio':
                                                                    await bot.send_audio(user_id_array[iiii], file_id_storage_array[j], caption=message_text)
                                                                case 'voice':
                                                                    await bot.send_voice(user_id_array[iiii], file_id_storage_array[j], caption=message_text)
                                                                case 'animation':
                                                                    await bot.send_animation(user_id_array[iiii], file_id_storage_array[j], caption=message_text)
                                                                case 'video_note':
                                                                    await bot.send_video_note(user_id_array[iiii], file_id_storage_array[j], caption=message_text)
                                                                case _:
                                                                    await bot.send_document(user_id_array[iiii], file_id_storage_array[j], caption=message_text)

                                                        except:
                                                            print(user_id_array[iiii], " User not found")


                                                        sql_delete = """Delete from add_file_storage where date_time = %s"""
                                                        cursor.execute(sql_delete, (dates_array_for_comparing[k],))

                                                        sql_update = ('''
                                                                        UPDATE add_file_storage
                                                                        SET date_time = %s
                                                                        WHERE date_time = %s
                                                                            ''')
                                                        s = (raw_dates_string[k][raw_dates_string[k].find(",") + 2 : ])
                                                        cursor.execute(sql_update, (s, raw_dates_string[k],))
                                                        connection.commit()