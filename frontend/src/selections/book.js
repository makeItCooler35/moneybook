export default
{
  title: "Книга операций",
  fields: [
    {
      key: 'sum',
      label: "Сумма"
    },
    {
      key: 'bonus',
      label: "Бонус"
    },
    {
      key: 'description',
      label: 'Описание'
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
    }
  ]
}