#!/bin/bash

Nom du fichier à créer
TEST_FILE="/tmp/test_installation.txt"

Message à écrire dans le fichier
echo "L'installation de ce script a réussi le $(date)." > "$TEST_FILE"

Afficher un message de succès
echo "Fichier de test créé avec succès à l'emplacement : $TEST_FILE"
