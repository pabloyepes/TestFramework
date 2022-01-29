class Utils(object):

    @staticmethod
    def get_scenario_tags(scenario):
        """
        List all tags for a specific scenario and it's feature
        :return: List   Scenario and Feature tags
        """
        tags = [{}]
        for tag in scenario.tags[:] + scenario.feature.tags[:]:
            tag.split('=')
            if '=' in tag:
                tag = tag.split('=')
                tags[0][tag[0]] = tag[1]
            else:
                tags.append(tag)

        return tags

    @staticmethod
    def row_to_dict(row):
        """
        Converts a behave.model.row into a dict
        :param row:     Row     Behaves row to convert
        :return:        Dict    Parsed data
        """
        d = {}
        for key, value in row.items():
            d[key] = value
        return d
