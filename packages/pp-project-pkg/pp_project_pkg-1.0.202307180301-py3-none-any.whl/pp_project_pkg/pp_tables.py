## extra functions
import wml.visionml as wv
import time

__all__ = ["queries","time_wrapper"]


def time_wrapper(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        print('time taken: {}'.format(end-start))
        return result
    return wrapper


class queries():
    def __init__(self,date = '2023-05-29',site_id= 30607 ,logger=None) :
          self.logger = logger
          self.query_list = ['hub_custom_breakdown','site_info','pp_driver_input','food_items','meal_period_configuration','pp_production','pp_rework','waste_data_for_site']
          self.date = date
          self.engine = wv.ml_engine
          self.date_start_time = date + ' 00:00:00'
          self.date_end_time = date + ' 23:59:59'
          self.site_id = site_id

    @time_wrapper
    def hub_custom_breakdown(self):
        q1 = "select cb.id,  cb.name from menu_mgmt.menu m,menu_mgmt.menu_custom_breakdown mcb,menu_mgmt.custom_breakdown cb where m.id  = mcb.menu_id and mcb.custom_breakdown_id = cb.id and m.id  = 100009181 "
        return wv.read_sql(q1,self.engine)

    @time_wrapper
    def site_info(self):
        q1 = """
        select
        l0.id, 
        l0.name as tracker_name, 
        l16.id, 
        l16.name as kitchen_name
            from winnow.location_closure lc
            inner join winnow.location l0 on lc.child_id = l0.id
            inner join winnow.location l16 on lc.parent_id = l16.id
            where lc.parent_id = {}
            and l0.level = 0 """.format(self.site_id)
        return wv.read_sql(q1,self.engine)

    @time_wrapper
    def pp_driver_input(self):
        q1 = """
    SELECT 
        vs.start_date, 
        vcs.site_id, 
        vmpc.meal_period, 
        vd.driver_type, 
        (jsonb_array_elements(vd.payload)::jsonb)->'label' AS label, 
        (jsonb_array_elements(vd.payload)::jsonb)->'value' AS value 
    FROM 
        pp_meal_service.view_drivers vd, 
        pp_meal_service.view_service vs, 
        pp_meal_service.view_meal_period_configuration vmpc, 
        pp_meal_service.view_current_state vcs 
    where vd.view_service_id  = vs.id 
    and vmpc.view_service_id = vs.id
    and vcs.id  = vs.view_current_state_id
    and vcs.site_id = {}
    and date(vs.start_date) = '{}'
    order by vs.start_date desc """.format(self.site_id,self.date)
        return wv.read_sql(q1,self.engine)

    @time_wrapper
    def food_items(self):
        q1 = """
        select fi.id as food_item_id, 
        fg.name as "food_group", 
        fi."name",
        fiwi.vision_food_item_id as waste_identifier,
        fi.taxonomy_code as taxonomy_code
        from 
            pp_configuration_service.site s
            inner join pp_configuration_service.site_configuration sc on s.id = sc.site_id
            inner join pp_configuration_service.meal_period_configuration mpc on sc.id = mpc.site_configuration_entity_id 
            inner join pp_configuration_service.menu_configuration mc on sc.id = mc.site_configuration_entity_id 
            inner join pp_configuration_service.food_group fg on mc.id = fg.menu_configuration_id
            inner join pp_configuration_service.food_item fi on fi.food_group_id = fg.id
            inner join pp_configuration_service.food_item_waste_identifier fiwi on fiwi.food_item_entity_id = fi.id
            where s.site_id = {} """.format(self.site_id)
        return wv.read_sql(q1,self.engine)

    @time_wrapper
    def meal_period_configuration(self):
        q1 = """select s.site_id, 
       mpc.waste_disposal_start_time, 
       mpc.waste_disposal_end_time, 
       mpc.meal_period  
       
  from pp_configuration_service.site s
		inner join pp_configuration_service.site_configuration sc on s.id = sc.site_id
		inner join pp_configuration_service.meal_period_configuration mpc on sc.id = mpc.site_configuration_entity_id
	 where s.site_id = {}""".format(self.site_id)
        return wv.read_sql(q1,self.engine)

    # @time_wrapper
    # def pp_production_rework(self):
    #     q1 = """select 
    # curr_state.site_id,
    # service.id as service_id,
    # service.start_date as meal_service_start_date,
    # meal_period_config.meal_period,
    # food_group.id as food_group_id, 
    # food_item.id as food_item_id, 
    # food_item."name",  
    # food_item_figures.taxonomy_code,
    # food_item_figures.unit, 
    # food_item_figures.figure_type, 
    # food_item_figures.quantity_kg as quantity_kg,
    #             (select vfir.quantity_kg  from pp_meal_service.view_food_item_rework vfir 
    #             where vfir.view_food_item_id = food_item.id
    #             and vfir.id = (select max(vfir.id)
    #                       from pp_meal_service.view_food_item_rework vfir, pp_meal_service.view_food_item fi
    #                       where vfir.view_food_item_id = fi.id
    #                       and vfir.view_food_item_id = food_item.id)) as rework, 
    #    food_item_figures.created as food_item_figure_created
    # from
    #     pp_meal_service.view_current_state curr_state, 
    #     pp_meal_service.view_service service,
    #     pp_meal_service.view_meal_period_configuration meal_period_config,
    #     pp_meal_service.view_food_group food_group,
    #     pp_meal_service.view_food_item food_item,
    #     pp_meal_service.view_food_item_figures food_item_figures

    #     where curr_state.id = service.view_current_state_id
    #     and service.id = food_group.view_service_id
    #     and meal_period_config.view_service_id = service.id
    #     and food_group.id = food_item.view_food_group_id
    #     and food_item.id = food_item_figures.view_food_item_id
    #     and food_item_figures.figure_type = 'PRODUCTION_ADJUSTMENT'
    #     and food_item_figures.id = (select max(vfif2.id) from pp_meal_service.view_food_item_figures vfif2 
    #             where food_item_figures.view_food_item_id  = vfif2.view_food_item_id)
    #     and curr_state.site_id = {}
    #     and service.start_date between '{}' and '{}'
    #     order by service.id desc
    #     """.format(self.site_id,self.date_start_time,self.date_end_time)
    #     return wv.read_sql(q1,self.engine)

    @time_wrapper
    def pp_production(self):
        q1 = """select 
        meal_service_id,
        taxonomy_code,
        actual_production_unit,
        actual_production_kg
        from (
            select 
            svc.id as meal_service_id,
            fi.taxonomy_code as taxonomy_code,
            fif.quantity_unit as actual_production_unit,
            fif.quantity_kg as actual_production_kg,
            rank() over (partition by svc.id, fif.taxonomy_code order by fif.created desc) as rnk
        from pp_meal_service.view_food_group as fg
        inner join pp_meal_service.view_food_item as fi on fi.view_food_group_id = fg.id
        inner join pp_meal_service.view_food_item_figures as fif on fif.view_food_item_id = fi.id
        inner join pp_meal_service.view_service as svc on svc.id = fg.view_service_id
        where svc.start_date between'{}' and '{}' 
        and figure_type = 'PRODUCTION_ADJUSTMENT'
        ) as ordered_figures
        where rnk = 1""".format(self.date_start_time,self.date_end_time)
        return wv.read_sql(q1,self.engine)

    @time_wrapper
    def pp_rework(self):
        q1="""SELECT
        meal_service_id,
        taxonomy_code,
        rework_unit,
        rework_kg
        from (
            select 
            svc.id as meal_service_id,
            fi.taxonomy_code as taxonomy_code,
            fir.quantity as rework_unit,
            fir.quantity_kg as rework_kg,
            rank() over (partition by svc.id, fir.view_food_item_id order by fir.created desc) as rnk
        from pp_meal_service.view_food_group as fg
        inner join pp_meal_service.view_food_item as fi on fi.view_food_group_id = fg.id
        inner join pp_meal_service.view_food_item_rework as fir on fir.view_food_item_id = fi.id
        inner join pp_meal_service.view_service as svc on svc.id = fg.view_service_id
        where svc.start_date between '{}' and '{}' 
        ) as ordered_figures
        where rnk = 1""".format(self.date_start_time,self.date_end_time)
        return wv.read_sql(q1,self.engine)


    @time_wrapper
    def waste_data_for_site(self):
        q1 = """select e.id,
       site_guid, 
       item_id, 
       reason_guid, 
       m.value as weight_g,
       local_time,
       e.created
        from winnow.event e 
        inner join winnow.measurement m on e.id = m.event_id
        inner join winnow.location l0 on e.site_guid = l0.id
        inner join winnow.location_closure lc on l0.id = lc.child_id
        where lc.parent_id = {}
            and l0.level = 0
            and e.local_time between '{}' and '{}'
            order by e.local_time desc;""".format(self.site_id,self.date_start_time,self.date_end_time)
        return wv.read_sql(q1,self.engine)
    
    def run_all(self):
            list_of_df = []
            for i in self.query_list:
                a = getattr(self,i)()
                if self.logger:
                    self.logger.info('query {} done'.format(i))
                list_of_df.append(a)
            return list_of_df