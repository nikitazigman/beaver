package middleware

import (
	"context"
	"net/http"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

const dbKey string = "dbTx"

func TransactionMiddleware(pool *pgxpool.Pool) func(next http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		fn := func(w http.ResponseWriter, r *http.Request) {
			ctx := r.Context()
			tx, err := pool.Begin(ctx)
			if err != nil {
				http.Error(w, "Could not start a transaction", http.StatusInternalServerError)
				return
			}
			defer func() {
				if p := recover(); p != nil {
					tx.Rollback(ctx)
					panic(p)
				}
			}()

			ctx = context.WithValue(r.Context(), dbKey, tx)
			next.ServeHTTP(w, r.WithContext(ctx))
			if err := tx.Commit(ctx); err != nil {
				http.Error(w, "Could not commit a transaction", http.StatusInternalServerError)
			}
		}
		return http.HandlerFunc(fn)
	}
}

func GetTransactionFromContext(ctx context.Context) pgx.Tx {
	tx, ok := ctx.Value(dbKey).(pgx.Tx)
	if !ok {
		panic("There is no transaction in the given context")
	}
	return tx
}
