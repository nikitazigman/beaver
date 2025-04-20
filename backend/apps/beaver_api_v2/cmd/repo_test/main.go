package main

import (
	"beaver-api/internal/db/scriptdetail"
	"context"
	"fmt"
	"os"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgtype"
)

const (
	fmtDBString = "host=%s user=%s password=%s dbname=%s port=%d sslmode=disable"
	host        = "localhost"
	user        = "beaver_api"
	password    = "beaver_api"
	dbname      = "beaver_api_db"
	port        = 5432
)

func main() {
	url := fmt.Sprintf(fmtDBString, host, user, password, dbname, port)

	conn, err := pgx.Connect(context.Background(), url)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close(context.Background())

	q := scriptdetail.New(conn)
	tagID, err := uuid.Parse("5a4aaf5c-c7ba-4e48-a776-b4e5e9342089")
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(tagID)
	qp := scriptdetail.RandomParams{
		TagIDs:     nil,
		LanguageID: pgtype.UUID{},
		ContribIDs: nil,
	}
	scripts, err := q.Random(context.Background(), qp)
	if err != nil {
		fmt.Print(err)
	}
	for i, script := range scripts {
		fmt.Println(i, script.ScriptTitle.String, script.LanguageName.String, script.TagName.String, script.ContributorName.String)
	}
}
