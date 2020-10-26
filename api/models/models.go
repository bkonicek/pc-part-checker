package models

import "go.mongodb.org/mongo-driver/bson/primitive"

// Part struct definition
type Part struct {
	ID    primitive.ObjectID `json:"_id,omitempty" bson:"_id,omitempty"`
	Name  string             `json:"name" bson:"name,omitempty"`
	Price int                `json:"price" bson:"price,omitempty"`
}
