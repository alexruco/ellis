# Ellis  🧠

Welcome to **Ellis**! This project is named in honor of Ellis Horowitz, a computer scientist and specialist in the history of computer languages. The module is designed to retrieve messages sent to an email from admin, user and AI, and organize messages in a thread.

## Features ✨

- **get_messages()**: Go to your inbox and return unread messages - Use a Conversation Key (conv_key) to organize messages in a thread. 🔥
- **get_history()**: Retrieve the full history based on the conv_key. 🎉

## Installation 💻

You can install the package via pip:

```bash
pip install git+https://github.com/alexruco/ellis
```

```python
from ellis import module
```
# Example usage
result = module.some_function(5, 10)
print(result)

L

## SQL

Here are the SQL commands used to create the necessary database tables for this module:

```sql
CREATE TABLE tb_conversation (
    id SERIAL PRIMARY KEY,
    conv_key VARCHAR(10) DEFAULT substr(md5(random()::text || clock_timestamp()::text), 1, 10) NOT NULL, -- Auto-generated hash as conversation key
    user_email TEXT NOT NULL,                        -- Comma-separated user email addresses
    system_email TEXT NOT NULL,                      -- Comma-separated system email addresses
    model_email TEXT NOT NULL,                       -- Comma-separated model email addresses
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp when the conversation was created
    status BOOLEAN DEFAULT TRUE                      -- Status of the conversation (active/inactive)
);

CREATE TABLE tb_conversation_history (
    id SERIAL PRIMARY KEY,
    conv_key VARCHAR(10) NOT NULL,              -- The conversation key this entry is associated with
    sender TEXT NOT NULL,                       -- The email address of the sender
    recipient TEXT NOT NULL,                    -- The email address of the recipient(s)
    sender_type VARCHAR(10) NOT NULL,           -- Type of sender: 'user', 'system', 'AI', or 'model'
    content TEXT NOT NULL,                      -- The content of the message
    attachment BYTEA,                           -- Attachment data (if any)
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When the message was sent/received
    email_hash VARCHAR(64) NOT NULL             -- Unique hash of the email content
);

CREATE TABLE IF NOT EXISTS public.tb_processed_emails (
    id INTEGER NOT NULL DEFAULT nextval('tb_processed_emails_id_seq'::regclass),
    email_hash VARCHAR(64) NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT tb_processed_emails_pkey PRIMARY KEY (id),
    CONSTRAINT tb_processed_emails_email_hash_key UNIQUE (email_hash)
);
```

### Contributing 🤝

We welcome contributions from the community! Here’s how you can get involved:

1. **Report Bugs**: If you find a bug, please open an issue [here](https://github.com/alexruco/ellis/issues).
2. **Suggest Features**: We’d love to hear your ideas! Suggest new features by opening an issue.
3. **Submit Pull Requests**: Ready to contribute? Fork the repo, make your changes, and submit a pull request. Please ensure your code follows our coding standards and is well-documented.
4. **Improve Documentation**: Help us improve our documentation. Feel free to make edits or add new content.

### How to Submit a Pull Request

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin my-feature-branch`.
5. Open a pull request on the original repository.

## License 📄

This project is licensed under the MIT License. Feel free to use, modify, and distribute this software in accordance with the terms outlined in the [LICENSE](LICENSE) file.
