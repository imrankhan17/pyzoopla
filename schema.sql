create table public.energy_certificates
(
	LMK_KEY varchar(30) not null
		primary key,
	ADDRESS1 text null,
	ADDRESS2 text null,
	ADDRESS3 text null,
	POSTCODE text null,
	BUILDING_REFERENCE_NUMBER bigint null,
	CURRENT_ENERGY_RATING text null,
	POTENTIAL_ENERGY_RATING text null,
	CURRENT_ENERGY_EFFICIENCY int null,
	POTENTIAL_ENERGY_EFFICIENCY int null,
	PROPERTY_TYPE text null,
	BUILT_FORM text null,
	INSPECTION_DATE date null,
	LOCAL_AUTHORITY text null,
	CONSTITUENCY text null,
	COUNTY text null,
	LODGEMENT_DATE date null,
	TRANSACTION_TYPE text null,
	ENVIRONMENT_IMPACT_CURRENT int null,
	ENVIRONMENT_IMPACT_POTENTIAL int null,
	ENERGY_CONSUMPTION_CURRENT int null,
	ENERGY_CONSUMPTION_POTENTIAL float null,
	CO2_EMISSIONS_CURRENT float null,
	CO2_EMISS_CURR_PER_FLOOR_AREA float null,
	CO2_EMISSIONS_POTENTIAL float null,
	LIGHTING_COST_CURRENT float null,
	LIGHTING_COST_POTENTIAL float null,
	HEATING_COST_CURRENT float null,
	HEATING_COST_POTENTIAL float null,
	HOT_WATER_COST_CURRENT float null,
	HOT_WATER_COST_POTENTIAL float null,
	TOTAL_FLOOR_AREA float null,
	ENERGY_TARIFF text null,
	MAINS_GAS_FLAG text null,
	FLOOR_LEVEL text null,
	FLAT_TOP_STOREY text null,
	FLAT_STOREY_COUNT int default 0 null,
	MAIN_HEATING_CONTROLS text null,
	MULTI_GLAZE_PROPORTION float null,
	GLAZED_TYPE text null,
	GLAZED_AREA text null,
	EXTENSION_COUNT int default 0 null,
	NUMBER_HABITABLE_ROOMS text null,
	NUMBER_HEATED_ROOMS int default -1 null,
	LOW_ENERGY_LIGHTING int default -1 null,
	NUMBER_OPEN_FIREPLACES int default -1 null,
	HOTWATER_DESCRIPTION text null,
	HOT_WATER_ENERGY_EFF text null,
	HOT_WATER_ENV_EFF text null,
	FLOOR_DESCRIPTION text null,
	FLOOR_ENERGY_EFF text null,
	FLOOR_ENV_EFF text null,
	WINDOWS_DESCRIPTION text null,
	WINDOWS_ENERGY_EFF text null,
	WINDOWS_ENV_EFF text null,
	WALLS_DESCRIPTION text null,
	WALLS_ENERGY_EFF text null,
	WALLS_ENV_EFF text null,
	SECONDHEAT_DESCRIPTION text null,
	SHEATING_ENERGY_EFF text null,
	SHEATING_ENV_EFF text null,
	ROOF_DESCRIPTION text null,
	ROOF_ENERGY_EFF text null,
	ROOF_ENV_EFF text null,
	MAINHEAT_DESCRIPTION text null,
	MAINHEAT_ENERGY_EFF text null,
	MAINHEAT_ENV_EFF text null,
	MAINHEATCONT_DESCRIPTION text null,
	MAINHEATC_ENERGY_EFF text null,
	MAINHEATC_ENV_EFF text null,
	LIGHTING_DESCRIPTION text null,
	LIGHTING_ENERGY_EFF text null,
	LIGHTING_ENV_EFF text null,
	MAIN_FUEL text null,
	WIND_TURBINE_COUNT int default -99 null,
	HEAT_LOSS_CORRIDOOR text null,
	UNHEATED_CORRIDOR_LENGTH float null,
	FLOOR_HEIGHT float null,
	PHOTO_SUPPLY float null,
	SOLAR_WATER_HEATING_FLAG text null,
	MECHANICAL_VENTILATION text null,
	ADDRESS text null,
	LOCAL_AUTHORITY_LABEL text null,
	CONSTITUENCY_LABEL text null,
	CERTIFICATE_HASH text null
)
;

create table for_sale_listings
(
	listing_id varchar(10) not null
		primary key,
	listing_price varchar(10) null,
	price_modifier mediumtext null,
	address mediumtext null,
	summary mediumtext null,
	num_beds tinytext null,
	num_baths tinytext null,
	num_receptions tinytext null,
	description text null,
	listing_date date null,
	estate_agent text null,
	station1 text null,
	distance1 float null,
	station2 text null,
	distance2 float null,
	date_generated timestamp(3) null
)
;

create table listings_description
(
	listing_id varchar(10) not null
		primary key,
	description longtext charset utf8 null,
	main_features longtext null,
	more_features longtext null,
	price_history text null,
	date_generated timestamp(3) null
)
;

create table public.price_paid
(
	id varchar(40) not null
		primary key,
	price_paid int(12) null,
	date datetime null,
	post_code varchar(10) null,
	property_type varchar(1) null,
	new_build varchar(1) null,
	estate_type varchar(1) null,
	saon text null,
	paon tinytext null,
	street text null,
	locality text null,
	town text null,
	district text null,
	county text null,
	category_type varchar(1) null,
	record_status varchar(1) null
)
;

create table property_details
(
	acorn_type varchar(10) null,
	activity varchar(255) null,
	country_code varchar(2) null,
	incode varchar(3) null,
	listing_id int null,
	location varchar(7) null,
	num_baths tinytext null,
	num_beds tinytext null,
	outcode varchar(4) null,
	page varchar(20) null,
	postal_area varchar(2) null,
	price tinytext null,
	price_estimate tinytext null,
	price_last_sale tinytext null,
	price_temptme varchar(10) null,
	property_type varchar(30) null,
	rental_value tinytext null,
	section varchar(30) null,
	address varchar(255) null,
	id int not null
		primary key,
	geolocation varchar(255) null,
	for_sale_id varchar(10) null,
	property_value varchar(255) null,
	value_change text null,
	sales_history text null,
	date_generated timestamp(3) null
)
;

create table to_rent_listings
(
	listing_id varchar(10) not null
		primary key,
	listing_price varchar(25) null,
	price_modifier mediumtext null,
	address mediumtext null,
	summary mediumtext null,
	num_beds tinytext null,
	num_baths tinytext null,
	num_receptions tinytext null,
	description text null,
	listing_date date null,
	estate_agent text null,
	station1 text null,
	distance1 float null,
	station2 text null,
	distance2 float null,
	date_generated timestamp(3) null
)
;

