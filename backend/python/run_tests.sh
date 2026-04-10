#!/bin/bash

echo "🧪 Starting test suite..."
coverage run manage.py test products

echo "📊 Generating coverage report..."
coverage report -m

echo "✅ Done!"
