function getBedNameByType(bedtype) {
	var name = '';
	switch(bedtype) {
		case 0:
			name = '单床';
			break;
		case 1:
			name = '大床';
			break;
		case 2:
			name = '双床';
			break;
		case 3:
			name = '三床';
			break;
		case 4:
			name = '三床-1大2单';
			break;
		case 5:
			name = '榻榻米';
			break;
		case 6:
			name = '拼床';
			break;
		case 7:
			name = '水床';
			break;
		case 8:
			name = '榻榻米双床';
			break;
		case 9:
			name = '榻榻米单床';
			break;
		case 10:
			name = '圆床';
			break;
		case 11:
			name = '上下铺';
			break;
		case 12:
			name = '大床或双床';
			break;
		case -1:
			name = '未知';
			break;
		default:
			name = '未知';
	}

	return name;
}
