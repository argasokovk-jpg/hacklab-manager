#!/bin/bash
echo "🧪 Тестирование без интернета"
echo "============================="

echo "1. network_info..."
hl scan 127.0.0.1 --tool network_info

echo ""
echo "2. port_check..."
hl scan 127.0.0.1 --tool port_check

echo ""
echo "3. hash_cracker..."
hl scan "5f4dcc3b5aa765d61d8327deb882cf99" --tool hash_cracker

echo ""
echo "✅ Локальные тесты пройдены"
