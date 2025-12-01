
CREATE TABLE company (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  hq_address TEXT,
  country_id INTEGER NOT NULL,
  branding_config TEXT CHECK (json_valid(branding_config)), -- requires SQLite JSON extension
  FOREIGN KEY (country_id) REFERENCES country(id)
);

CREATE INDEX idx_company_country_id ON company(country_id);

CREATE TABLE country (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  code TEXT NOT NULL UNIQUE
);

CREATE TABLE venue (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  size_in_square_feet NUMERIC CHECK (size_in_square_feet >= 0),
  latitude NUMERIC CHECK (latitude BETWEEN -90 AND 90),
  longitude NUMERIC CHECK (longitude BETWEEN -180 AND 180),
  country_id INTEGER NOT NULL,
  FOREIGN KEY (country_id) REFERENCES country(id)
);

CREATE INDEX idx_venue_country_id ON venue(country_id);

CREATE TABLE ghg_scope (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE emission_category (
  id INTEGER PRIMARY KEY,
  category TEXT NOT NULL UNIQUE
);

CREATE TABLE event (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  start_time TEXT NOT NULL,
  end_time TEXT NOT NULL,
  company_id INTEGER NOT NULL,
  venue_id INTEGER NOT NULL,
  total_attendees INTEGER NOT NULL DEFAULT 0 CHECK (total_attendees >= 0),
  virtual_attendees INTEGER NOT NULL DEFAULT 0 CHECK (virtual_attendees >= 0),
  physical_attendees_local INTEGER NOT NULL DEFAULT 0 CHECK (physical_attendees_local >= 0),
  physical_attendees_international INTEGER NOT NULL DEFAULT 0 CHECK (physical_attendees_international >= 0),
  total_event_hour INTEGER CHECK (total_event_hour IS NULL OR total_event_hour >= 0),
  total_catering_count INTEGER CHECK (total_catering_count IS NULL OR total_catering_count >= 0),
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  CHECK (end_time >= start_time),
  CHECK (
    total_attendees = (
      virtual_attendees +
      physical_attendees_local +
      physical_attendees_international
    )
  ),
  FOREIGN KEY (company_id) REFERENCES company(id),
  FOREIGN KEY (venue_id) REFERENCES venue(id)
);

CREATE INDEX idx_event_company_id ON event(company_id);
CREATE INDEX idx_event_venue_id ON event(venue_id);
CREATE INDEX idx_event_start_time ON event(start_time);

CREATE TABLE emission (
  id INTEGER PRIMARY KEY,
  event_id INTEGER NOT NULL,
  activity_value NUMERIC,
  activity_unit TEXT,
  category_id INTEGER NOT NULL,
  scope INTEGER NOT NULL CHECK (scope IN (1, 2, 3)),
  calculated_emission_in_kgC02e NUMERIC,

  FOREIGN KEY (event_id) REFERENCES event(id),
  FOREIGN KEY (category_id) REFERENCES emission_category(id),
  FOREIGN KEY (scope) REFERENCES ghg_scope(id)
);


CREATE INDEX idx_emission_event_id ON emission(event_id);
CREATE INDEX idx_emission_category_id ON emission(category_id);
