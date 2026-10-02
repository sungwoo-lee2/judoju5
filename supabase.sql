create table if not exists public.leader_finder_state (
  id text primary key,
  payload jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create or replace function public.set_leader_finder_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists trg_leader_finder_updated_at on public.leader_finder_state;
create trigger trg_leader_finder_updated_at
before update on public.leader_finder_state
for each row execute function public.set_leader_finder_updated_at();

-- Render 무료 서버 재시작 후에도 KRX 과거 일별 자료를 복원하기 위한 영구 표
create table if not exists public.krx_history_days (
  market text not null,
  day text not null,
  payload jsonb not null default '[]'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (market, day)
);

create index if not exists idx_krx_history_days_day
on public.krx_history_days (day desc);
