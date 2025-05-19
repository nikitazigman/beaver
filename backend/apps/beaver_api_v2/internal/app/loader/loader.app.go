package loader

import (
	"beaver-api/internal/business/loader"
	"beaver-api/utils/middleware"
	"encoding/json"
	"net/http"
)

type Controller struct {
	s *loader.Service
}

func new(s *loader.Service) *Controller {
	return &Controller{
		s: s,
	}
}

func (c *Controller) LoadScripts(w http.ResponseWriter, r *http.Request) {
	var dto []POSTUpdateScriptDTO

	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&dto)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	scriptDetail, t, err := toScriptDetail(dto)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	tx := middleware.GetTransactionFromContext(r.Context())
	err = c.s.LoadScripts(r.Context(), tx, scriptDetail, t)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
	}
	w.WriteHeader(http.StatusCreated)
}

func (c *Controller) DeleteScripts(w http.ResponseWriter, r *http.Request) {
	var dto POSTDeleteScriptDTO
	logger := middleware.GetLoggerFromContext(r.Context())
	logger.Info("test logger")
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&dto)
	if err != nil {
		logger.Info(err)
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	timestamp, err := toTimestamp(dto)
	if err != nil {
		logger.Info(err)
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	tx := middleware.GetTransactionFromContext(r.Context())
	if err := c.s.RemoveOldScripts(r.Context(), tx, timestamp); err != nil {
		logger.Info(err)
		w.WriteHeader(http.StatusBadRequest)
	}
	w.WriteHeader(http.StatusNoContent)
}
