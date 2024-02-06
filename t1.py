from bardapi import Bard


token = 'g.a000gAhkcysjsLAeooAvwY-EETErIZ3QWF3LbWjgHy8nkVJCpHONeP5T0XW3WkJAM_vLXTV4ywACgYKAbISAQASFQHGX2Mi5mbilUXDGrHnJttU0IoJQhoVAUF8yKqI5xGrgHwhm20X_RbEHOh40076.'
bard = Bard(token=token)

# bard = Bard(token_from_browser=True)

response = bard.get_answer("Do you like cookies?")

print(response['content'])