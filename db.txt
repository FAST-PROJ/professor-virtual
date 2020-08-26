create database crawler;
use crawler;

create table urls (
	id_url int not null auto_increment,
    url varchar(1000) not null,
    constraint pk_urls_id_url primary key (id_url)
);
create index idx_urls_url on urls (url);

create table words (
	id_word int not null auto_increment,
    word varchar(200) not null,
    constraint pk_words_word primary key (id_word)
);
create index idx_words_word on words (word);

create table word_location (
	id_word_location int not null auto_increment,
    id_url int not null,
    id_word int not null,
    location_page int,
    constraint pk_id_word_location primary key (id_word_location),
    constraint fk_word_location_id_url foreign key (id_url) references urls (id_url),
    constraint fk_word_location_id_word foreign key (id_word) references words (id_word)
);
create index idx_word_location_id_word on word_location (id_word);

alter database crawler character set = utf8mb4 collate = utf8mb4_unicode_ci;
alter table words convert to character set utf8mb4 collate utf8mb4_unicode_ci;
alter table words modify column word varchar(200) character set utf8mb4 collate utf8mb4_unicode_ci;