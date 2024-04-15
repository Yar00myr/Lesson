from sqlalchemy import create_engine, String, DateTime, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, sessionmaker
from datetime import datetime


engine = create_engine("sqlite:///my.sql", echo=True)


class Base(DeclarativeBase):
    unit_id: Mapped[int] = mapped_column(primary_key=True)
    


class Event(Base):
    __tablename__ = "event"
    unit_id: Mapped[int] = mapped_column(primary_key=True)
    typeof: Mapped[str] = mapped_column(String(30))
    start: Mapped[datetime] = mapped_column(DateTime)
    end: Mapped[datetime] = mapped_column(DateTime)
    result: Mapped[bool]

    def result(self) :
        return f"<Type: {self.typeof}, Start: {self.start}, End: {self.end}, Result: {self.result}>"



Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


typeof = input("Введіть назву: ")
start = datetime.strptime(input("Введіть час початку: "), "%Y-%m-%d %H:%M")
end = datetime.strptime(input("Введіть час завершення: "), "%Y-%m-%d %H:%M")
result = input("Введіть статус (так / ні): ")
if result == "так":
    result = True
else:
    result = False


start_filter = datetime.strptime(input("Введіть час запуску фільтрації: "), "%Y-%m-%d %H:%M")
end_filter = datetime.strptime(input("Введіть час завершення фільтрації: "), "%Y-%m-%d %H:%M")


with Session() as session:
    event = Event(typeof=typeof, start=start, end=end, result=result)
    session.add(event)
    events = session.scalars(select(Event).where(Event.start >= start_filter).where(Event.end <= end_filter)).all()
    finished = None
    total_events = len(events)
    for event in events:
        if event.result == True:
            finished += 1
    winrate = (finished / total_events) * 100 if total_events > 0 else 0
    print(f"Всього подій: {total_events}, Закінчено: {finished}, Рейтинг: {winrate}%.")
    session.commit()