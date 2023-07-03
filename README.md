# AWSCostReporter

AWSCostReporter is a Python script that automates the process of fetching cost data from AWS Cost Explorer, applying filters, exporting the data to a CSV file, and sending the file via email. It's designed to be user-friendly and is particularly useful for keeping track of AWS costs over a period of three months.

## Features

- Fetches cost data from AWS Cost Explorer.
- Applies filters to the data:
  - Charge Type (excludes: credit, saving plan negation, tax).
  - Billing Entity (includes only: AWS).
- Exports the data to a CSV file.
- Sends the CSV file via email.
- Displays the results in the terminal in a tabular format.

## Requirements

- Python 3.x
- AWS Account with Cost Explorer enabled
- AWS Access Key and Secret Key with permissions to access Cost Explorer
- Email account for sending reports

## Installation

1. Clone the repository:

git clone https://github.com/bobbycvi/AWSCostReporter.git

2. Change to the directory:

cd AWSCostReporter

3. Install the required Python libraries:

pip install boto3 tabulate pandas

## Configuration

1. Set your AWS credentials as environment variables:

export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key

2. Edit the script to include your email credentials and recipient email address.

## Usage

Run the script:

python AWSCostReporter.py

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
