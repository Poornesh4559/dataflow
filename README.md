# dataflow

gcloud auth application-default login

gcloud services enable dataflow.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud config set builds/use_kaniko True
gcloud config get-value project

TEMPLATE_IMAGE = gcr.io/smart-quasar-342413/dataflow/my_pipeline:latest
PROJECT_ID = smart-quasar-342413
TEMPLATE_PATH = gs://${BUCKET}/templates/mytemplate.json

gcloud builds submit --tag gcr.io/{PROJECT_ID}/dataflow/my_pipeline:latest

gcloud beta dataflow flex-template build gs://smart-quasar-342413/templates/mytemplate.json --image gcr.io/{PROJECT_ID}/dataflow/my_pipeline:latest --sdk-language "PYTHON" --metadata-file "metadata.json"


gcloud dataflow flex-template run first-try-flex-tempate --region us-central1 --template-file-gcs-location gs://sample-data-bkt1/templates/mytemplate.json --parameters input=gs://us-bkt-1/sampledata.csv --parameters output=smart-quasar-342413:sink_csv.emp

