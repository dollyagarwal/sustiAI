

-- Insert Countries
INSERT INTO country (id, name, code) VALUES (1, 'Singapore', 'SG');
INSERT INTO country (id, name, code) VALUES (2, 'United States', 'US');
INSERT INTO country (id, name, code) VALUES (3, 'United Kingdom', 'UK');
INSERT INTO country (id, name, code) VALUES (4, 'India', 'IN');
INSERT INTO country (id, name, code) VALUES (5, 'Germany', 'DE');

-- Insert Venues
INSERT INTO venue (id, name, size_in_square_feet, latitude, longitude, country_id) VALUES (1, 'Marina Bay Convention Center', 50000, 1.283, 103.86, 1);
INSERT INTO venue (id, name, size_in_square_feet, latitude, longitude, country_id) VALUES (2, 'New York Expo Hall', 75000, 40.7128, -74.006, 2);
INSERT INTO venue (id, name, size_in_square_feet, latitude, longitude, country_id) VALUES (3, 'London Event Hub', 60000, 51.5074, -0.1278, 3);
INSERT INTO venue (id, name, size_in_square_feet, latitude, longitude, country_id) VALUES (4, 'Mumbai Grand Hall', 45000, 19.076, 72.8777, 4);
INSERT INTO venue (id, name, size_in_square_feet, latitude, longitude, country_id) VALUES (5, 'Berlin Conference Center', 55000, 52.52, 13.405, 5);

-- Insert GHG Scopes
INSERT INTO ghg_scope (id, name, description) VALUES (1, 'Scope 1', 'Direct emissions from owned or controlled sources');
INSERT INTO ghg_scope (id, name, description) VALUES (2, 'Scope 2', 'Indirect emissions from purchased electricity, steam, heating, and cooling');
INSERT INTO ghg_scope (id, name, description) VALUES (3, 'Scope 3', 'All other indirect emissions that occur in the value chain');

-- Insert Emission Categories
INSERT INTO emission_category (id, category) VALUES (1, 'Travel');
INSERT INTO emission_category (id, category) VALUES (2, 'Accommodation');
INSERT INTO emission_category (id, category) VALUES (3, 'Catering');
INSERT INTO emission_category (id, category) VALUES (4, 'Venue Energy');
INSERT INTO emission_category (id, category) VALUES (5, 'Materials');
INSERT INTO emission_category (id, category) VALUES (6, 'Waste');
INSERT INTO emission_category (id, category) VALUES (7, 'Digital');

INSERT INTO company (id, name, country_id, branding_config) 
VALUES (1, 'BlueSky Corp', 1, '{"primary_color": "#007bff", "logo_url": "https://png.pngtree.com/png-clipart/20190604/original/pngtree-corporate-image-logo-png-image_1026060.jpg"}');

INSERT INTO company (id, name, country_id, branding_config) 
VALUES (2, 'NextGen Solutions', 2, '{"primary_color": "#dc3545", "logo_url": "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/company-logo-design-template-e089327a5c476ce5c70c74f7359c5898_screen.jpg?ts=1672291305"}');

INSERT INTO company (id, name, country_id, branding_config) 
VALUES (3, 'EcoSphere Ltd', 3, '{"primary_color": "#28a745", "logo_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbBL29Jawxl9ELLRe8K5Qgy0udooluQC2NQQ&s"}');

INSERT INTO company (id, name, country_id, branding_config) 
VALUES (4, 'Visionary Group', 4, '{}'); -- '{}' is the minimum valid JSON if no data exists

INSERT INTO company (id, name, country_id, branding_config) 
VALUES (5, 'GreenEdge Inc', 5, '{"primary_color": "#ffc107"}');


-- Insert Events
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (1, 'Product Launch', 'Product Launch for company 5', '2024-12-27 00:00', '2024-12-27 06:00', 5, 1, 457, 50, 328, 79, 6, 407);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (2, 'Sustainability Summit', 'Sustainability Summit for company 4', '2025-11-05 00:00', '2025-11-05 09:00', 4, 1, 364, 14, 220, 130, 9, 350);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (3, 'Tech Expo', 'Tech Expo for company 3', '2024-05-13 00:00', '2024-05-13 07:00', 3, 2, 623, 129, 123, 371, 7, 494);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (4, 'Annual Strategy Meeting', 'Annual Strategy Meeting for company 3', '2024-10-09 00:00', '2024-10-09 09:00', 3, 4, 184, 2, 145, 37, 9, 182);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (5, 'Tech Expo', 'Tech Expo for company 3', '2025-01-01 00:00', '2025-01-01 06:00', 3, 5, 228, 1, 157, 70, 6, 227);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (6, 'Innovation Workshop', 'Innovation Workshop for company 3', '2025-02-06 00:00', '2025-02-06 08:00', 3, 4, 108, 22, 69, 17, 8, 86);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (7, 'Quarterly Business Review', 'Quarterly Business Review for company 3', '2025-01-15 00:00', '2025-01-15 08:00', 3, 1, 300, 21, 233, 46, 8, 279);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (8, 'Quarterly Business Review', 'Quarterly Business Review for company 1', '2024-01-01 00:00', '2024-01-01 09:00', 1, 2, 229, 30, 157, 42, 9, 199);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (9, 'Sustainability Summit', 'Sustainability Summit for company 5', '2025-11-07 00:00', '2025-11-07 06:00', 5, 2, 102, 13, 54, 35, 6, 89);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (10, 'Innovation Workshop', 'Innovation Workshop for company 3', '2024-07-07 00:00', '2024-07-07 07:00', 3, 1, 312, 2, 46, 264, 7, 310);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (11, 'Sustainability Summit', 'Sustainability Summit for company 1', '2024-06-25 00:00', '2024-06-25 06:00', 1, 4, 111, 23, 22, 66, 6, 88);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (12, 'Sustainability Summit', 'Sustainability Summit for company 5', '2025-05-25 00:00', '2025-05-25 09:00', 5, 4, 504, 67, 33, 404, 9, 437);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (13, 'Product Launch', 'Product Launch for company 1', '2025-02-26 00:00', '2025-02-26 07:00', 1, 4, 722, 48, 629, 45, 7, 674);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (14, 'Annual Strategy Meeting', 'Annual Strategy Meeting for company 2', '2025-11-07 00:00', '2025-11-07 07:00', 2, 1, 196, 7, 176, 13, 7, 189);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (15, 'Sustainability Summit', 'Sustainability Summit for company 2', '2024-07-26 00:00', '2024-07-26 07:00', 2, 4, 387, 122, 87, 178, 7, 265);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (16, 'Quarterly Business Review', 'Quarterly Business Review for company 3', '2024-03-29 00:00', '2024-03-29 10:00', 3, 1, 111, 31, 19, 61, 10, 80);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (17, 'Quarterly Business Review', 'Quarterly Business Review for company 1', '2024-09-08 00:00', '2024-09-08 07:00', 1, 1, 513, 126, 169, 218, 7, 387);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (18, 'Product Launch', 'Product Launch for company 2', '2024-01-24 00:00', '2024-01-24 10:00', 2, 5, 661, 19, 582, 60, 10, 642);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (19, 'Annual Strategy Meeting', 'Annual Strategy Meeting for company 2', '2024-09-04 00:00', '2024-09-04 09:00', 2, 3, 713, 134, 197, 382, 9, 579);
INSERT INTO event (id, name, description, start_time, end_time, company_id, venue_id, total_attendees, virtual_attendees, physical_attendees_local, physical_attendees_international, total_event_hour, total_catering_count) VALUES (20, 'Quarterly Business Review', 'Quarterly Business Review for company 4', '2024-11-04 00:00', '2024-11-04 10:00', 4, 3, 221, 58, 42, 121, 10, 163);

-- Insert Emissions
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (1, 1, 48595.50, 'kWh', 1, 3, 5350.80);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (2, 1, 26779.20, 'km', 2, 1, 14533.04);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (3, 1, 49364.61, 'km', 3, 2, 2144.22);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (4, 1, 3756.14, 'GB', 4, 3, 10290.22);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (5, 1, 28105.40, 'GB', 5, 2, 18802.94);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (6, 1, 43663.09, 'GB', 6, 1, 2240.31);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (7, 1, 13579.48, 'kg', 7, 3, 10471.57);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (8, 2, 22912.83, 'room_nights', 1, 1, 15033.84);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (9, 2, 36766.18, 'kWh', 2, 1, 12847.46);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (10, 2, 7160.82, 'GB', 3, 3, 14348.38);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (11, 2, 30543.04, 'meals', 4, 1, 18439.46);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (12, 2, 32051.52, 'room_nights', 5, 1, 17696.87);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (13, 2, 2924.13, 'kg', 6, 1, 1216.95);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (14, 2, 32505.21, 'km', 7, 3, 5584.21);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (15, 3, 44291.07, 'meals', 1, 2, 3793.69);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (16, 3, 30246.28, 'room_nights', 2, 3, 18638.51);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (17, 3, 14038.01, 'GB', 3, 1, 1297.67);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (18, 3, 11481.20, 'GB', 4, 2, 15897.03);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (19, 3, 44816.70, 'GB', 5, 3, 19749.89);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (20, 3, 3866.07, 'kWh', 6, 3, 13644.03);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (21, 3, 12837.34, 'room_nights', 7, 3, 1106.18);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (22, 4, 18069.65, 'GB', 1, 2, 4771.06);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (23, 4, 30215.62, 'room_nights', 2, 3, 19475.79);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (24, 4, 4521.13, 'km', 3, 3, 5721.74);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (25, 4, 49806.93, 'meals', 4, 2, 9473.36);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (26, 4, 28999.41, 'kWh', 5, 3, 8406.30);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (27, 4, 31501.98, 'km', 6, 2, 11252.03);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (28, 4, 36160.74, 'kg', 7, 1, 5798.10);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (29, 5, 2110.78, 'kg', 1, 1, 19075.49);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (30, 5, 32484.80, 'GB', 2, 1, 8276.27);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (31, 5, 16850.31, 'km', 3, 2, 19814.13);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (32, 5, 6529.12, 'km', 4, 2, 14203.92);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (33, 5, 35034.40, 'km', 5, 1, 5026.69);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (34, 5, 11304.64, 'kWh', 6, 3, 10212.68);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (35, 5, 3388.09, 'kWh', 7, 1, 12829.54);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (36, 6, 28992.83, 'GB', 1, 3, 10695.62);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (37, 6, 7404.03, 'km', 2, 3, 15668.61);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (38, 6, 2371.90, 'GB', 3, 1, 14325.29);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (39, 6, 5384.83, 'GB', 4, 3, 19181.75);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (40, 6, 29869.18, 'kg', 5, 1, 4906.06);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (41, 6, 13763.05, 'meals', 6, 3, 9485.72);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (42, 6, 872.27, 'kWh', 7, 3, 15816.14);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (43, 7, 32193.24, 'GB', 1, 2, 5265.25);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (44, 7, 40645.36, 'km', 2, 3, 18758.62);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (45, 7, 24117.26, 'kg', 3, 2, 1037.01);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (46, 7, 14349.23, 'meals', 4, 1, 7982.58);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (47, 7, 10131.20, 'kWh', 5, 3, 16338.99);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (48, 7, 43261.77, 'km', 6, 1, 3098.68);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (49, 7, 24519.25, 'meals', 7, 1, 4323.55);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (50, 8, 46795.02, 'kg', 1, 3, 3908.10);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (51, 8, 1480.31, 'kg', 2, 3, 18163.21);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (52, 8, 15287.90, 'km', 3, 2, 17181.19);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (53, 8, 4929.31, 'kWh', 4, 2, 8344.17);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (54, 8, 42438.10, 'km', 5, 2, 4356.03);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (55, 8, 48365.97, 'room_nights', 6, 1, 16858.48);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (56, 8, 9150.32, 'room_nights', 7, 3, 8986.91);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (57, 9, 17322.79, 'meals', 1, 1, 18359.67);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (58, 9, 48292.42, 'GB', 2, 2, 5432.64);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (59, 9, 49100.86, 'kg', 3, 3, 1605.79);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (60, 9, 38784.18, 'km', 4, 2, 11356.68);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (61, 9, 36393.71, 'km', 5, 1, 6811.63);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (62, 9, 7906.38, 'kg', 6, 3, 16873.12);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (63, 9, 7600.25, 'meals', 7, 2, 19784.72);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (64, 10, 36143.03, 'GB', 1, 1, 5553.41);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (65, 10, 5456.89, 'meals', 2, 2, 12737.33);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (66, 10, 27080.89, 'km', 3, 2, 5055.10);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (67, 10, 6778.61, 'GB', 4, 1, 19634.85);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (68, 10, 20621.69, 'kWh', 5, 3, 6703.28);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (69, 10, 29953.75, 'kWh', 6, 3, 8956.63);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (70, 10, 34399.97, 'kWh', 7, 1, 9849.06);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (71, 11, 7140.13, 'meals', 1, 2, 6039.64);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (72, 11, 11650.09, 'kg', 2, 2, 19019.48);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (73, 11, 20429.16, 'kg', 3, 3, 18714.67);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (74, 11, 16901.95, 'kWh', 4, 1, 14652.68);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (75, 11, 10853.12, 'meals', 5, 3, 18677.07);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (76, 11, 35572.90, 'kWh', 6, 1, 8123.60);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (77, 11, 25514.96, 'meals', 7, 1, 19100.67);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (78, 12, 47765.38, 'GB', 1, 3, 5462.50);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (79, 12, 38337.61, 'kWh', 2, 1, 5067.85);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (80, 12, 46111.00, 'GB', 3, 2, 1203.87);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (81, 12, 20091.07, 'kWh', 4, 2, 13485.03);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (82, 12, 35527.57, 'meals', 5, 1, 269.88);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (83, 12, 25245.43, 'km', 6, 1, 19215.03);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (84, 12, 11011.54, 'room_nights', 7, 1, 16774.39);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (85, 13, 7199.41, 'kWh', 1, 3, 2441.11);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (86, 13, 25628.17, 'kWh', 2, 1, 15120.04);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (87, 13, 14801.38, 'km', 3, 2, 14862.47);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (88, 13, 7042.25, 'km', 4, 2, 19077.65);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (89, 13, 25943.26, 'kg', 5, 1, 257.32);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (90, 13, 26032.59, 'meals', 6, 2, 154.29);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (91, 13, 1278.63, 'room_nights', 7, 2, 8299.17);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (92, 14, 11173.25, 'kWh', 1, 1, 17856.81);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (93, 14, 20885.94, 'room_nights', 2, 1, 12272.55);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (94, 14, 19427.12, 'GB', 3, 2, 7736.17);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (95, 14, 40017.43, 'kWh', 4, 1, 7889.05);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (96, 14, 48326.48, 'km', 5, 3, 14336.11);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (97, 14, 7326.83, 'kWh', 6, 2, 4456.71);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (98, 14, 1751.19, 'meals', 7, 2, 2765.11);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (99, 15, 16242.22, 'room_nights', 1, 1, 10656.89);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (100, 15, 40318.00, 'kg', 2, 3, 16231.81);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (101, 15, 11952.77, 'km', 3, 1, 612.08);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (102, 15, 36757.74, 'kg', 4, 2, 17702.81);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (103, 15, 15273.82, 'room_nights', 5, 2, 3485.83);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (104, 15, 16284.82, 'meals', 6, 1, 4400.02);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (105, 15, 4972.34, 'room_nights', 7, 1, 8390.95);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (106, 16, 6630.54, 'room_nights', 1, 3, 5085.17);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (107, 16, 14655.30, 'kWh', 2, 2, 5120.64);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (108, 16, 46272.27, 'room_nights', 3, 3, 16012.30);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (109, 16, 35172.49, 'meals', 4, 1, 13299.05);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (110, 16, 42429.89, 'km', 5, 1, 5173.75);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (111, 16, 8382.10, 'kWh', 6, 2, 9192.28);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (112, 16, 28047.83, 'room_nights', 7, 3, 9941.08);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (113, 17, 11369.16, 'GB', 1, 2, 15847.95);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (114, 17, 24503.93, 'kg', 2, 1, 16961.50);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (115, 17, 46323.78, 'GB', 3, 1, 8135.26);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (116, 17, 24345.43, 'kWh', 4, 2, 5927.89);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (117, 17, 38423.20, 'room_nights', 5, 2, 6367.74);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (118, 17, 11737.65, 'kWh', 6, 2, 16633.34);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (119, 17, 15664.11, 'kWh', 7, 1, 4451.16);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (120, 18, 297.55, 'km', 1, 3, 7579.19);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (121, 18, 24224.27, 'kWh', 2, 1, 5777.43);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (122, 18, 927.94, 'kg', 3, 1, 18056.37);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (123, 18, 17958.54, 'kWh', 4, 3, 1259.54);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (124, 18, 17978.22, 'kWh', 5, 1, 14964.01);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (125, 18, 38076.26, 'meals', 6, 1, 18583.21);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (126, 18, 29592.78, 'room_nights', 7, 3, 12846.17);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (127, 19, 4466.81, 'GB', 1, 3, 19635.37);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (128, 19, 30270.49, 'room_nights', 2, 3, 2227.05);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (129, 19, 25386.77, 'kg', 3, 3, 17838.11);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (130, 19, 36081.89, 'kg', 4, 2, 14814.63);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (131, 19, 44925.25, 'kg', 5, 1, 6756.75);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (132, 19, 15585.50, 'GB', 6, 1, 107.84);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (133, 19, 24531.55, 'meals', 7, 3, 1614.62);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (134, 20, 8987.46, 'GB', 1, 1, 4110.79);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (135, 20, 32431.25, 'kg', 2, 1, 2827.85);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (136, 20, 39441.33, 'GB', 3, 3, 13119.80);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (137, 20, 8188.84, 'meals', 4, 3, 2225.04);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (138, 20, 25259.04, 'km', 5, 1, 15986.02);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (139, 20, 29103.57, 'kg', 6, 2, 16201.69);
INSERT INTO emission (id, event_id, activity_value, activity_unit, category_id, scope, calculated_emission_in_kgC02e) VALUES (140, 20, 15488.80, 'GB', 7, 1, 6725.58);
