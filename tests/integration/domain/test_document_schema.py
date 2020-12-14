#  Copyright (c) 2019 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.
import os
from datetime import datetime

import firefly_survey.domain as domain


async def test_simple_survey(client, registry, container, serializer):
    os.environ['ANONYMOUS_ACCESS'] = 'true'

    validator = container.validator
    schemas = registry(domain.Schema)
    documents = registry(domain.Document)

    schema = domain.Schema(schema={
        '$schema': 'http://json-schema.org/draft-07/schema',
        'type': 'object',
        'title': 'My Firefly Survey',
        'description': 'A survey for Firefly users',
        'properties': {
            'question_1': {
                '$id': '#/properties/question_1',
                'type': 'boolean',
                'title': 'True or False - I enjoy using Firefly.',
                'description': 'Whether or not you enjoy using the Firefly framework.',
                'default': True,
            }
        }
    })
    schemas.append(schema)
    schemas.commit()

    await client.post('/firefly-survey/documents', data=serializer.serialize({
        'data': {
            'question_1': True,
        },
        'schema': schema.id,
    }))

    document = documents[0]

    assert document.question_1 is True
    assert isinstance(document.created_on, datetime)
    result = validator.validate(document, against=schema)
    assert result['count'] == 0
