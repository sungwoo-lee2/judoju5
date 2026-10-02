-- Supabase > SQL Editor에서 한 번만 실행하세요.
-- Render 무료 서버가 재시작되어도 KRX 과거 데이터를 유지합니다.
create table if not exists public.krx_history_days (
  market text not null,
  day text not null,
  payload jsonb not null default '[]'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (market, day)
);

create index if not exists idx_krx_history_days_day
on public.krx_history_days (day desc);
