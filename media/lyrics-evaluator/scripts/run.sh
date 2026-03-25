#!/bin/bash

# 输入参数
INPUT="$1"

# 轻量分析（节奏 + 押韵）
LINES=$(echo "$INPUT" | sed '/^$/d')
LINE_COUNT=$(echo "$LINES" | wc -l)

# 句长统计
LENGTHS=$(echo "$LINES" | awk '{print length}')
AVG=$(echo "$LENGTHS" | awk '{sum+=$1} END {print sum/NR}')
STD=$(echo "$LENGTHS" | awk -v avg=$AVG '{sum+=($1-avg)^2} END {print sqrt(sum/NR)}')

# 节奏分数
if [ "$AVG" = "0" ]; then
  RHYTHM=0
else
  RHYTHM=$(awk -v std=$STD -v avg=$AVG 'BEGIN {print 1 - std/avg}')
fi

# 押韵（简单尾字统计）
LAST_CHARS=$(echo "$LINES" | awk '{print substr($0,length,1)}')
TOP_FREQ=$(echo "$LAST_CHARS" | sort | uniq -c | sort -nr | head -n1 | awk '{print $1}')
RHYME=$(awk -v top=$TOP_FREQ -v total=$LINE_COUNT 'BEGIN {print top/total}')

# 构造增强输入
ENHANCED=$(cat <<EOF
{
  "lyrics": "$INPUT",
  "analysis": {
    "rhythm_score": $RHYTHM,
    "rhyme_score": $RHYME,
    "line_count": $LINE_COUNT
  }
}
EOF
)

# 输出给 skill engine（由 engine 调用 LLM）
echo "$ENHANCED"
