PROJECT=xenomorph
PLAN_DIR=plans
PLAN_FILE=$(PLAN_DIR)/apply-plan.out
DESTROY_FILE=$(PLAN_DIR)/destroy-plan.out

all: plan

$(PLAN_DIR):
	mkdir -p $(PLAN_DIR)

plan: $(PLAN_DIR)
	terraform plan -out $(PLAN_FILE) -backend-config="project=$(PROJECT)"
	terraform plan -destroy -out $(DESTROY_FILE) -backend-config="project=$(PROJECT)"
	terraform show $(PLAN_FILE) -backend-config="project=$(PROJECT)"

apply: 
	terraform apply $(PLAN_FILE) -backend-config="project=$(PROJECT)"

destroy: $(PLAN_DIR)
	terraform apply $(DESTROY_FILE) -backend-config="project=$(PROJECT)"

