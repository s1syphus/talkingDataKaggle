
SET GLOBAL innodb_lock_wait_timeout = 3600; 

insert into train_data_with_labels (device_id, group_name, label_id, is_installed, is_active)
select gender_age_train_index.device_id, gender_age_train_index.group, e.label_id, is_installed, is_active from
    gender_age_train_index
    join
    (
          select talking_data.events.device_id, l.app_id, l.is_installed, l.is_active, l.label_id from
                  talking_data.events join
          (select blah.app_id, app_events_index.event_id, blah.label_id, app_events_index.is_installed, app_events_index.is_active from
          app_events_index
          join (
                          select app_id, label_categories_index.label_id from label_categories_index join app_labels_index on label_categories_index.label_id = app_labels_index.label_id
              ) as blah
              on blah.app_id = app_events_index.app_id
          ) as l
          on talking_data.events.event_id = l.event_id
          ) as e
 on e.device_id = gender_age_train_index.device_id;
 
 
 