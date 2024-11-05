# TechQwest

A comprehensive Flask-based IT knowledge question management and distribution system with user authentication, performance tracking, and personalized learning paths.

## Features

- **User Authentication**: Secure login and registration system
- **Daily Questions**: Daily IT knowledge questions for consistent learning
- **Performance Tracking**: Track user progress with skill levels and success rates
- **Personalized Learning**: Adaptive difficulty based on user performance
- **Analytics Dashboard**: Comprehensive statistics and performance visualization
- **Admin Interface**: Question management and category administration

## Technical Stack

- **Backend**: Flask, PostgreSQL
- **Frontend**: Bootstrap 5 (Dark Theme)
- **Authentication**: Flask-Login
- **Database Management**: SQLAlchemy, Flask-Migrate
- **Charts**: Chart.js

## Setup Instructions

1. Clone the repository
2. Set up environment variables:
   ```
   DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]
   FLASK_SECRET_KEY=[your-secret-key]
   ```

3. Install dependencies:
   ```bash
   pip install flask flask-sqlalchemy flask-migrate flask-login psycopg2-binary
   ```

4. Initialize the database:
   ```bash
   flask db upgrade
   python create_admin.py  # Creates initial admin user
   python update_categories.py  # Sets up default categories
   ```

5. Run the application:
   ```bash
   python app.py
   ```

## Project Structure

```
.
├── app.py                 # Application entry point
├── models.py             # Database models
├── forms.py             # Form definitions
├── routes/              # Route blueprints
│   ├── admin.py        # Admin panel routes
│   ├── auth.py         # Authentication routes
│   ├── questions.py    # Question management
│   └── analytics.py    # Analytics dashboard
├── templates/          # Jinja2 templates
├── static/            # Static files
└── migrations/        # Database migrations
```

## Features in Detail

### User System
- Registration and authentication
- Skill level progression
- Performance tracking
- Streak counting

### Question Management
- Multiple difficulty levels
- Category organization
- Daily question rotation
- Answer tracking

### Analytics
- Success rate visualization
- Category performance analysis
- Progress tracking
- Skill level progression

### Admin Interface
- Question creation and management
- Category management
- User progress monitoring
- System statistics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - free to use and modify
