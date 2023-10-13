# MyApp: Example Fuzzy Search App

An example fuzzy search app, with fuzzy search accessible via the `/fuzzy_search` endpoint.

Uses LevelDB to store search related information and constructs an FST to perform the fuzzy search. The FST currently
has a state limit, meaning the max distance parameter should be small.

The app runs a Kafka consumer in the background and will automatically pull in data as it arrives in Kafka. Another
background process rebuild the FST when new data is received, waiting to rebuild until a minute has passed since the
last update to LevelDB.
