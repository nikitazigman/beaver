package middleware

import (
	"context"
	"log"
	"net/http"
	"time"

	"github.com/go-chi/chi/v5/middleware"
	"go.uber.org/zap"
)

func LoggerMiddleware(logger *zap.SugaredLogger) func(next http.Handler) http.Handler {
	if logger == nil {
		log.Panic("Logger was not provided to the logger middleware")
	}

	return func(next http.Handler) http.Handler {
		fn := func(w http.ResponseWriter, r *http.Request) {
			ww := middleware.NewWrapResponseWriter(w, r.ProtoMajor)
			t1 := time.Now()
			requestId := middleware.GetReqID(r.Context())
			reqLogger := logger.With(
				zap.String("proto", r.Proto),
				zap.String("path", r.URL.Path),
				zap.String("request_id", requestId),
			)
			ctx := context.WithValue(r.Context(), loggerKey, reqLogger)

			defer func() {
				reqLogger = reqLogger.With(
					zap.Duration("latency seconds", time.Duration(time.Since(t1))),
					zap.Int("status", ww.Status()),
					zap.Int("size bytes", ww.BytesWritten()),
				)
				reqLogger.Info("Served")
			}()
			next.ServeHTTP(ww, r.WithContext(ctx))
		}
		return http.HandlerFunc(fn)
	}
}

func GetLoggerFromContext(ctx context.Context) *zap.SugaredLogger {
	logger, ok := ctx.Value(loggerKey).(*zap.SugaredLogger)
	if !ok {
		return zap.NewNop().Sugar()
	}
	return logger
}
