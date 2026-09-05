create table users
(
    id         varchar(36) primary key,
    email      varchar(255) unique not null,
    role       varchar(20)         not null,
    first_name varchar(50)         not null,
    last_name  varchar(50)         not null,
    grade      tinyint             not null,
    created_at timestamp default current_timestamp
);

create table conversations
(
    id         varchar(36) primary key,
    user_id    varchar(36) not null,
    status     varchar(20) not null,
    created_at timestamp default current_timestamp,
    foreign key (user_id) references users (id)
);
CREATE INDEX idx_conversations_user_id
    ON conversations (user_id);

create table messages
(
    id              varchar(36) primary key,
    conversation_id varchar(36) not null,
    role            varchar(20) not null,
    content         text        not null,
    created_at      timestamp default current_timestamp,
    foreign key (conversation_id) references conversations (id)
);
CREATE INDEX idx_messages_conversation_id
ON messages(conversation_id);