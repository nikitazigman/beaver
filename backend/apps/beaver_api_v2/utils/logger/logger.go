package logger

import (
	"go.uber.org/zap"
)

func New(isDebug bool) *zap.SugaredLogger {
	config := zap.NewProductionConfig()
	level := zap.InfoLevel
	if isDebug {
		level = zap.DebugLevel
	}
	config.Level = zap.NewAtomicLevelAt(level)

	return zap.Must(config.Build()).Sugar()
}
