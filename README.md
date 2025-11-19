# Twilio WhatsApp Sandbox Backend (TWS Backend)

Backend API developed with FastAPI to manage WhatsApp conversations through Twilio. The system implements a guided conversation flow that collects product review information from users.

## 📋 Description

This project is a backend that processes WhatsApp messages through Twilio webhooks. It implements a state-based conversation system that guides users through a structured questionnaire to collect:

- User name
- Product name
- Product review
- Future contact preference
- Preferred contact method

The system maintains the state of each conversation in the database, allowing users to continue from where they left off if they interrupt the conversation.

## ✨ Features

- **State-based conversation flow**: Robust system that maintains each user's progress
- **Flexible validations**: Accepts response variations (yes/YES/Yeah, no/NO/Nope)
- **State persistence**: Conversation progress is never lost
- **Data validation**: Complete validations for all fields
- **Error handling**: Clear and helpful error messages
- **RESTful API**: Endpoints to manage reviews
- **PostgreSQL database**: Persistent data storage
- **Alembic migrations**: Database version control

## 🛠️ Technologies Used

- **Python 3.13**
- **FastAPI**: Modern and fast web framework
- **SQLAlchemy**: ORM for Python
- **PostgreSQL**: Relational database
- **Alembic**: Database migration tool
- **Twilio**: WhatsApp integration
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

## 📦 Prerequisites

Before starting, make sure you have installed:

- Python 3.11 or higher
- PostgreSQL 12 or higher
- Git
- Twilio account with WhatsApp Sandbox access

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/tws_backend.git
cd tws_backend
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

**Example:**
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/tws_db
```

**Optional Twilio Variables (for future features):**
```env
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

> **Note:** The Twilio variables are optional. Currently, the webhook only receives and responds to messages. These variables would be needed if you want to send proactive messages or validate webhook signatures in the future.

### 5. Create the Database

Make sure PostgreSQL is running and create the database:

```sql
CREATE DATABASE tws_db;
```

### 6. Run Migrations

Apply migrations to create tables in the database:

```bash
alembic upgrade head
```

### 7. Start the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`

## 📁 Project Structure

```
tws_backend/
├── alembic/                  # Database migrations
│   └── versions/            # Migration files
├── app/
│   ├── controllers/         # Business logic (CRUD)
│   │   ├── conversation_crud.py
│   │   └── reviews_crud.py
│   ├── database/            # Database configuration
│   │   ├── database.py
│   │   └── crud.py
│   ├── models/              # SQLAlchemy models
│   │   ├── conversation_state.py
│   │   ├── review.py
│   │   └── allModels.py
│   ├── routes/              # API endpoints
│   │   ├── reviews_router.py
│   │   └── twilio_webhook.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── conversation_state.py
│   │   └── review.py
│   ├── service/             # Service logic
│   │   └── conversation_service.py
│   └── main.py              # Application entry point
├── alembic.ini              # Alembic configuration
├── requirements.txt         # Project dependencies
└── README.md               # This file
```

## 🔌 API Endpoints

### Health Check

```http
GET /
```

**Response:**
```json
{
  "message": "API TWS_BACKEND is running"
}
```

### Reviews

#### List all reviews
```http
GET /reviews/
```

#### Get a review by ID
```http
GET /reviews/{review_id}
```

#### Create a new review
```http
POST /reviews/
Content-Type: application/json

{
  "contact_number": "+1234567890",
  "user_name": "John Doe",
  "product_name": "Product X",
  "product_review": "Great product!",
  "preferred_contact_method": "WhatsApp",
  "preferred_contact_again": true
}
```

#### Update a review
```http
PUT /reviews/{review_id}
Content-Type: application/json

{
  "contact_number": "+1234567890",
  "user_name": "John Doe",
  "product_name": "Product X",
  "product_review": "Updated review",
  "preferred_contact_method": "Email",
  "preferred_contact_again": false
}
```

#### Delete a review
```http
DELETE /reviews/{review_id}
```

### Twilio Webhook

```http
POST /twilio/webhook
```

This endpoint receives WhatsApp messages from Twilio. It should not be called directly, but configured in the Twilio dashboard.

## 💬 Conversation Flow

The system implements a guided conversation flow with the following steps:

1. **WAITING_NAME**: Requests the user's name
2. **WAITING_PRODUCT_NAME**: Requests the product name
3. **WAITING_PRODUCT_REVIEW**: Requests the product review
4. **WAITING_CONTACT_AGAIN**: Asks if they want to be contacted again
5. **WAITING_CONTACT_METHOD**: If they answer "yes", requests the preferred contact method
6. **COMPLETED**: Conversation completed, review saved

### Validations

- **Name**: Minimum 2 characters, maximum 128. Allows letters, spaces, hyphens, and apostrophes.
- **Product name**: Minimum 2 characters, maximum 256.
- **Review**: Minimum 10 characters, maximum 5000.
- **Future contact**: Accepts yes/no variations (yes, y, yeah, sure, ok, no, n, nope, etc.)
- **Contact method**: Minimum 2 characters, maximum 128. Accepts common methods (WhatsApp, Email, Phone, etc.)

### Special Commands

- **restart**: Restarts the conversation from the beginning

## 🗄️ Database

### Table: `reviews`

Stores completed user reviews.

| Field | Type | Description |
|-------|------|-------------|
| review_id | Integer | Unique ID (PK) |
| contact_number | String(64) | Phone number |
| user_name | String(128) | User name |
| product_name | String(256) | Product name |
| product_review | Text | Product review |
| preferred_contact_method | String(128) | Preferred contact method |
| preferred_contact_again | Boolean | Whether they want to be contacted again |
| created_at | DateTime | Creation date |
| updated_at | DateTime | Update date |

### Table: `conversation_states`

Stores the current state of each conversation.

| Field | Type | Description |
|-------|------|-------------|
| state_id | Integer | Unique ID (PK) |
| contact_number | String(64) | Phone number (UNIQUE) |
| current_step | Enum | Current conversation step |
| user_name | String(128) | Name (temporarily stored) |
| product_name | String(256) | Product name (temporarily stored) |
| product_review | Text | Review (temporarily stored) |
| wants_contact_again | String(10) | Yes/no response |
| preferred_contact_method | String(128) | Preferred contact method |
| created_at | DateTime | Creation date |
| updated_at | DateTime | Update date |

## 🔧 Twilio Configuration

1. Access your Twilio account
2. Go to **Messaging** > **Settings** > **WhatsApp Sandbox**
3. Configure the webhook URL: `https://your-domain.com/twilio/webhook`
4. Save changes

### Twilio Environment Variables

If you want to use Twilio features in the future (sending proactive messages, validating webhooks), you'll need these variables in your `.env` file:

- **TWILIO_ACCOUNT_SID**: Your Twilio Account SID (found in Twilio Console)
- **TWILIO_AUTH_TOKEN**: Your Twilio Auth Token (found in Twilio Console)
- **TWILIO_WHATSAPP_NUMBER**: Your Twilio WhatsApp number (format: `whatsapp:+14155238886`)

> **Note:** Currently, these variables are not required for the webhook to work. The webhook receives messages and responds using TwiML, which doesn't require authentication. These variables would be needed for advanced features like sending messages programmatically or validating webhook signatures.

## 📝 Migrations

### Create a new migration

```bash
alembic revision --autogenerate -m "migration description"
```

### Apply migrations

```bash
alembic upgrade head
```

### Revert migration

```bash
alembic downgrade -1
```

## 🧪 Development

### Run in development mode

```bash
uvicorn app.main:app --reload
```

The `--reload` flag automatically reloads the server when it detects code changes.

### API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🐛 Troubleshooting

### Error: "DATABASE_URL is not set"

Make sure you have a `.env` file in the project root with the `DATABASE_URL` variable configured.

### Error: "relation does not exist"

Run migrations:
```bash
alembic upgrade head
```

### Database connection error

Verify that:
- PostgreSQL is running
- Credentials in `.env` are correct
- The database exists

## 📄 License

This project is open source and available under the MIT license.

## 👥 Contributing

Contributions are welcome. Please:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue in the GitHub repository.

---

**Developed with ❤️ using FastAPI and Twilio**