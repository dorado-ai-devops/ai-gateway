IMAGE_NAME=ai-gateway
VERSION=v0.1.22
CLUSTER_NAME=devops-ai
REGISTRY=localhost:5000
HELM_VALUES=../devops-ai-lab/manifests/helm-gateway/values.yaml
ARGO_APP_NAME=ai-gateway

.PHONY: all build tag push load update-values sync release run

all: build load

build:
	docker build --no-cache -t $(IMAGE_NAME):$(VERSION) .

tag:
	docker tag $(IMAGE_NAME):$(VERSION) $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

push: tag
	docker push $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

load:
	kind load docker-image $(IMAGE_NAME):$(VERSION) --name $(CLUSTER_NAME)

update-values:
	sed -i "s/^ *tag: .*/  tag: $(VERSION)/" $(HELM_VALUES)

sync:
	argocd app sync $(ARGO_APP_NAME)

release: build load update-values sync
	@echo "Release completo: $(IMAGE_NAME):$(VERSION) desplegado y sincronizado con ArgoCD."

run:
	docker run -p 5000:5000 $(IMAGE_NAME):$(VERSION)
