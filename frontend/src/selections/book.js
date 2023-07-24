export default
{
  title: "Книга операций",
  fields: [
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
      key: 'category_name',
      label: 'Категория',
      type: 'link',
      bindField: 'category'
    },
    {
      key: 'time_at',
      label: 'Дата и время',
      type: 'datetime'
    }
  ]
}