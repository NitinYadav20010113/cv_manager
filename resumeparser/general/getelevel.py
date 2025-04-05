def getedulevelid(level):

    if ('diploma' in level.lower()):
        return 1
    if ('graduation' in level.lower() or 'grad' in level.lower() or 'ug' in level.lower()):
        return 2
    if ('postgraduation' in level.lower() or 'post graduation' in level.lower() or 'pg' in level.lower() or 'postgrad' in level.lower() or 'post grad' in level.lower()):
        return 3
    if ('phd' in level.lower()):
        return 4
    if ('intermediate' in level.lower()):
        return 5
    if ('ssc' in level.lower() or's secondary' in level.lower() or 'senior secondary' in level.lower() or 's.secondary' in level.lower() or '12' in level.lower() or '12th' in level.lower()):
        return 6
    if ('hsc' in level.lower() or 'metric'  in level.lower() or'secondary' in level.lower() or '10' in level.lower() or '10th' in level.lower()):
        return 7
    