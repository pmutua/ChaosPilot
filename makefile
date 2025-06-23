# Load .env file
include .env
export

deploy:
	gcloud run deploy $(AGENT_SERVICE_NAME) \
		--source . \
		--region $(GOOGLE_CLOUD_LOCATION) \
		--allow-unauthenticated \
		--port=8000 \
		--set-env-vars "GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT),GOOGLE_CLOUD_LOCATION=$(GOOGLE_CLOUD_LOCATION),GOOGLE_GENAI_USE_VERTEXAI=$(GOOGLE_GENAI_USE_VERTEXAI), MODEL=$(MODEL),TOOLBOX_URL=$(TOOLBOX_URL),GOOGLE_API_KEY=$(GOOGLE_API_KEY)"

delete:
	gcloud run services delete $(AGENT_SERVICE_NAME) --region $(GOOGLE_CLOUD_LOCATION)
