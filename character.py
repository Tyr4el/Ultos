class Character:
    def __init__(self, level, physique, cunning, spirit, skills, masteries, patch):
        self.level = level
        self.physique = physique
        self.cunning = cunning
        self.spirit = spirit
        self.skills = skills
        self.masteries = masteries
        self.patch = patch

    @classmethod
    def convert_json_to_char_data(cls, json):
        return cls(
            level=json['data']['bio']['level'],
            physique=json['data']['bio']['physique'],
            cunning=json['data']['bio']['cunning'],
            spirit=json['data']['bio']['spirit'],
            skills=json['data']['skills'],
            masteries=json['data']['masteries'],
            patch=json['created_for_build']
        )
