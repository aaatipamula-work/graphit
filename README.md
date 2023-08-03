# Graphit

A simple graph generation API

## Deploy

**Note**: Navigate to home directory.

Run it in development with Flask:

```sh
flask --app main run
```

or 

```sh
python3 -m flask --app main run
```

## Endpoints

There are 2 endpoints:

- `/blob/image/{imageid}`
  - `GET` method 
  - Returns PNG image
- `/api/generate/graph`
  - `POST` method
  - Generates and graph image from JSON request body
  - JSON Schema:
    ```json
    {
        "chart_title": "Chart Title Here",
        "x_axis": "Name of X-Axis", // (Not required if type = "pie")
        "y_axis": "Name of Y-Axis", // (Not required if type = "pie")
        "columns": { 
            "ColumnName1": 1,
            "ColumnName2": 2,
        }, // (Column values must be integers, can repeat for any number of columns)
        "type": "pie" // (Must be "pie" or "bar")
    }
    ```
  - Redirects to `/blob/image/{imageid}`
