create table transactions (
  id serial primary key,
  user_name text not null,
  amount decimal(20,10) not null,
  amount_usd decimal(20,2) not null,
  currency text not null,
  message text null,
  blockchain_address text not null,
  blockchain_network text not null,
  status text not null,
  created_at timestamp not null default now(),
  private_key TEXT not null
);