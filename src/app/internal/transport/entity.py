class Entity:
    def __str__(self):
        result = [i + ": " + str(getattr(self, i))
                  for i in vars(self)]
        return "\n".join(result)
