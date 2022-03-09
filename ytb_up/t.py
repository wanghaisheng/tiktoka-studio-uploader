   if release_offset and not release_offset == "":
        print('mode a sta')
        if not int(release_offset.split('-')[0]) == 0:
            offset = timedelta(months=int(release_offset.split(
                '-')[0]), days=int(release_offset.split('-')[-1]))
        else:
            offset = timedelta(days=1)
        if publish_date is None:
            publish_date =datetime(
                date.today().year,  date.today().month,  date.today().day, 10, 15)
        publish_date += offset
    
    else:
        if publish_date is None:
            publish_date =datetime(
                date.today().year,  date.today().month,  date.today().day, 10, 15)
            offset = timedelta(days=1)  
        else:
            publish_date = publish_date
        dailycount=4

        release_offset=str(int(start_index/30))+'-'+str(int(start_index)/int(setting['dailycount']))
        
