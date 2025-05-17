package middleware

import (
	"net/http"
	"strings"
)

func TokenAuthMiddleware(secret string) func(next http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		fn := func(w http.ResponseWriter, r *http.Request) {
			token_header := r.Header.Get("Authorization")

			token := strings.Split(token_header, " ")
			if len(token) != 2 || token[1] != secret {
				http.Error(w, "Not authorized", http.StatusUnauthorized)
			}

			next.ServeHTTP(w, r)
		}
		return http.HandlerFunc(fn)
	}
}
