package storage

import (
	"fmt"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

const fmtDBString = "host=%s user=%s password=%s dbname=%s port=%d sslmode=disable"

func NewDB(host string, port int, user string, password string, dbname string) (*gorm.DB, error) {
	dsn := fmt.Sprintf(fmtDBString, host, user, password, dbname, port)
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	fmt.Println(dsn)
	if err != nil {
		return nil, err
	}
	fmt.Println(db)
	return db, nil
}
