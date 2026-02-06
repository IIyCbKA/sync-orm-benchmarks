import os

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def main() -> None:
  """
  Pony ORM does not support true bulk update as of 16.01.2026.
  Therefore, Test 11 "Bulk update" is skipped for Pony,
  and we mark it with a dash in benchmarks.
  """

  print(
    f'PonyORM. Test 11. Bulk update. {COUNT} entities\n'
    f'Bulk update is not supported'
  )


if __name__ == '__main__':
  main()