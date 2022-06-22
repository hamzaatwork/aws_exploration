# aws_exploration

## Set up
Please run following command to install dependencies
```
pip install -r requirements.txt
```

Link to visualization: [inet-henge](https://github.com/codeout/inet-henge)

Instal inet-henge using npm command
```
npm install inet-henge
```

Run inet-henge server using:
```
python -m http.server
```

## Usage
- Run **main.py** to collect data, data is stored in *discovery_reports.json*
- After collection, run **visualize.py** to make mapping data which is stored in *visualizable_data.json*
- Run inet-henge visualization server and view mapping on localhost:8000
