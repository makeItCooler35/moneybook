const fields = [
  {
    key: 'sum',
    label: "Сумма",
    type: 'number'
  },
  {
    key: 'bonus',
    label: "Бонус",
    type: 'number'
  },
  {
    key: 'description',
    label: 'Описание',
    type: 'text'
  },
  {
    key: 'category__name',
    label: 'Категория',
    type: 'link',
    bindField: 'category',
    bindKey: 'name',
    model: 'categories',
  },
  {
    key: 'time_at',
    label: 'Дата и время',
    type: 'datetime',
    formatter: value => {
      return new Date(value).toLocaleString('ru', {
        year: 'numeric',
        month: "numeric",
        day: "numeric",
        hour: 'numeric',
        minute: 'numeric'
      });
    }
  }
];

for(const item of fields) {
  item.sortable = true;
  item.class = 'text-center';
}

export default
{
  title: "Книга операций",
  fields
}