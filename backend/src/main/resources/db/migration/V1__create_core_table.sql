CREATE TABLE classified_data (
id BIGSERIAL PRIMARY KEY,

```
file_name VARCHAR(255) NOT NULL,
file_type VARCHAR(100),
file_size BIGINT,

classification_label VARCHAR(100),
confidence_score DECIMAL(5,2),

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

);

CREATE INDEX idx_file_name ON classified_data(file_name);
CREATE INDEX idx_classification_label ON classified_data(classification_label);
CREATE INDEX idx_created_at ON classified_data(created_at);
