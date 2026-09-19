import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as file:
        players_data = json.load(file)

        for players_name, players_info in players_data.items():
            guild_data = players_info.get("guild")
            guild_obj = None
            if guild_data:
                guild_obj, _ = Guild.objects.get_or_create(
                    name=guild_data["name"],
                    defaults={"description": guild_data.get("description")}
                )

            race_data = players_info["race"]
            race_obj, _ = Race.objects.get_or_create(
                name=race_data["name"],
                defaults={"description": race_data.get("description")}
            )

            skills_data = race_data["skills"]
            for skills_data in skills_data:
                Skill.objects.get_or_create(
                    name=skills_data["name"],
                    defaults={
                        "bonus": skills_data["bonus"],
                        "race": race_obj
                    }
                )

            Player.objects.get_or_create(
                nickname=players_name,
                defaults={
                    "email": players_info["email"],
                    "bio": players_info["bio"],
                    "race": race_obj,
                    "guild": guild_obj
                }
            )


if __name__ == "__main__":
    main()
