import numpy as np
from numba import njit
###################### DATE_SYMBOL ########################
@njit(cache=True)
def create_pkey_date_symbol_jit(records,count,pkey,dateiniidx,dateendidx,dateunit,start):
	n = pkey.size-1
	for i in range(start,count):
		intdt = np.int32(np.int64(records['date'][i])/dateunit)
		if dateiniidx[intdt]==-1:
			dateiniidx[intdt] = i
		if dateendidx[intdt]<i:
			dateendidx[intdt] = i
		h0 = hash(records['date'][i])
		h1 = hash(records['symbol'][i])
		h = (h0^h1)%n
		if pkey[h] == -1:
			pkey[h] = i
		else:
			duplicatedkey=True
			j=1
			while (\
				(records[pkey[h]]['date'] != records[i]['date']) |
				(records[pkey[h]]['symbol'] != records[i]['symbol'])
			):
				h = (h + j**2) % n
				if pkey[h]==-1:
					pkey[h]=i
					duplicatedkey=False
					break
				j+=1
			if duplicatedkey:
				raise Exception('error duplicated index')

@njit(cache=True)
def get_loc_date_symbol_jit(records,pkey,keys):
	n = pkey.size-1
	loc = np.empty((keys.size, ))
	for i in range(keys.size):
		h0 = hash(keys['date'][i])
		h1 = hash(keys['symbol'][i])
		h = (h0^h1)%n
		if pkey[h] == -1:
			loc[i] = pkey[h]
		else:
			j=1
			while (\
				(records[pkey[h]]['date'] != keys[i]['date']) |
				(records[pkey[h]]['symbol'] != keys[i]['symbol'])
			):
				h = (h + j**2) % n
				if pkey[h]==-1:
					break
				j+=1
			loc[i]=pkey[h]
	return loc

@njit(cache=True)
def upsert_date_symbol_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit):
	minchgid = count
	maxsize = records.size
	nrec = new_records.size
	loc = get_loc_date_symbol_jit(records, pkey, new_records)
	# new items
	isnew = new_records[loc==-1]
	if isnew.size > 0:
		minchgid = int(count)
		addsize = min(maxsize - count, isnew.size)
		count += addsize
		records[minchgid:count] = isnew[0:addsize]
		create_pkey_date_symbol_jit(records, count, pkey, dateiniidx, dateendidx, dateunit, minchgid)
	# existing items
	if isnew.size < nrec:
		minchgid = min(loc[loc>-1])
		for i in range(nrec):
			if loc[i] != -1:
				records[int(loc[i])] = new_records[i]
	return count, minchgid

###################### DATE_SYMBOL1_SYMBOL2 ########################
@njit(cache=True)
def create_pkey_date_symbol1_symbol2_jit(records,count,pkey,dateiniidx,dateendidx,dateunit,start):
	n = pkey.size-1
	for i in range(start,count):
		intdt = np.int32(np.int64(records['date'][i])/dateunit)
		if dateiniidx[intdt]==-1:
			dateiniidx[intdt] = i
		if dateendidx[intdt]<i:
			dateendidx[intdt] = i
		if records['symbol1'][i]!=records['symbol2'][i]:
			h0 = hash(records['date'][i])
			h1 = hash(records['symbol1'][i])
			h2 = hash(records['symbol2'][i])
			h = (h0^h1^h2)%n
		else:
			h0 = hash(records['date'][i])
			h1 = hash(records['symbol1'][i])
			h = (h0^h1)%n
		if pkey[h] == -1:
			pkey[h] = i
		else:
			duplicatedkey=True
			j=1
			while (\
				(records[pkey[h]]['date'] != records[i]['date']) |
				(records[pkey[h]]['symbol1'] != records[i]['symbol1']) |
				(records[pkey[h]]['symbol2'] != records[i]['symbol2'])
			):
				h = (h + j**2) % n
				if pkey[h]==-1:
					pkey[h]=i
					duplicatedkey=False
					break
				j+=1
			if duplicatedkey:
				raise Exception('error duplicated index')

@njit(cache=True)
def get_loc_date_symbol1_symbol2_jit(records,pkey,keys):
	n = pkey.size-1
	loc = np.empty((keys.size, ))
	for i in range(keys.size):
		if keys['symbol1'][i]!=keys['symbol2'][i]:
			h0 = hash(keys['date'][i])
			h1 = hash(keys['symbol1'][i])
			h2 = hash(keys['symbol2'][i])
			h = (h0^h1^h2)%n
		else:
			h0 = hash(keys['date'][i])
			h1 = hash(keys['symbol1'][i])
			h = (h0^h1)%n
		if pkey[h] == -1:
			loc[i] = pkey[h]
		else:
			j=1
			while (\
				(records[pkey[h]]['date'] != keys[i]['date']) |
				(records[pkey[h]]['symbol1'] != keys[i]['symbol1']) |
				(records[pkey[h]]['symbol2'] != keys[i]['symbol2'])
			):
				h = (h + j**2) % n
				if pkey[h]==-1:
					break
				j+=1
			loc[i]=pkey[h]
	return loc

@njit(cache=True)
def upsert_date_symbol1_symbol2_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit):
	minchgid = count
	maxsize = records.size
	nrec = new_records.size
	loc = get_loc_date_symbol1_symbol2_jit(records, pkey, new_records)
	# new items
	isnew = new_records[loc==-1]
	if isnew.size > 0:
		minchgid = int(count)
		addsize = min(maxsize - count, isnew.size)
		count += addsize
		records[minchgid:count] = isnew[0:addsize]
		create_pkey_date_symbol1_symbol2_jit(records, count, pkey, dateiniidx, dateendidx, dateunit, minchgid)
	# existing items
	if isnew.size < nrec:
		minchgid = min(loc[loc>-1])
		for i in range(nrec):
			if loc[i] != -1:
				records[int(loc[i])] = new_records[i]
	return count, minchgid

###################### DATE_PORTFOLIO ########################
@njit(cache=True)
def create_pkey_date_portfolio_jit(records,count,pkey,dateiniidx,dateendidx,dateunit,start):
	n = pkey.size-1
	for i in range(start,count):
		intdt = np.int32(np.int64(records['date'][i])/dateunit)
		if dateiniidx[intdt]==-1:
			dateiniidx[intdt] = i
		if dateendidx[intdt]<i:
			dateendidx[intdt] = i
		h0 = hash(records['date'][i])
		h1 = hash(records['portfolio'][i])
		h = (h0^h1)%n
		if pkey[h] == -1:
			pkey[h] = i
		else:
			duplicatedkey=True
			j=1
			while (\
				(records[pkey[h]]['date'] != records[i]['date']) |
				(records[pkey[h]]['portfolio'] != records[i]['portfolio'])
			):
				h = (h + j**2) % n
				if pkey[h]==-1:
					pkey[h]=i
					duplicatedkey=False
					break
				j+=1
			if duplicatedkey:
				raise Exception('error duplicated index')

@njit(cache=True)
def get_loc_date_portfolio_jit(records,pkey,keys):
	n = pkey.size-1
	loc = np.empty((keys.size, ))
	for i in range(keys.size):
		h0 = hash(keys['date'][i])
		h1 = hash(keys['portfolio'][i])
		h = (h0^h1)%n
		if pkey[h] == -1:
			loc[i] = pkey[h]
		else:
			j=1
			while (\
				(records[pkey[h]]['date'] != keys[i]['date']) |
				(records[pkey[h]]['portfolio'] != keys[i]['portfolio'])
			):
				h = (h + j**2) % n
				if pkey[h]==-1:
					break
				j+=1
			loc[i]=pkey[h]
	return loc

@njit(cache=True)
def upsert_date_portfolio_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit):
	minchgid = count
	maxsize = records.size
	nrec = new_records.size
	loc = get_loc_date_portfolio_jit(records, pkey, new_records)
	# new items
	isnew = new_records[loc==-1]
	if isnew.size > 0:
		minchgid = int(count)
		addsize = min(maxsize - count, isnew.size)
		count += addsize
		records[minchgid:count] = isnew[0:addsize]
		create_pkey_date_portfolio_jit(records, count, pkey, dateiniidx, dateendidx, dateunit, minchgid)
	# existing items
	if isnew.size < nrec:
		minchgid = min(loc[loc>-1])
		for i in range(nrec):
			if loc[i] != -1:
				records[int(loc[i])] = new_records[i]
	return count, minchgid

###################### DATE_PORTFOLIO_SYMBOL ########################
@njit(cache=True)
def create_pkey_date_portfolio_symbol_jit(records,count,pkey,dateiniidx,dateendidx,dateunit,portiniidx,portendidx,portlist,portlistcount,start):
	n = pkey.size-1
	for i in range(start,count):
		intdt = np.int32(np.int64(records['date'][i])/dateunit)
		if dateiniidx[intdt]==-1:
			dateiniidx[intdt] = i
		if dateendidx[intdt]<i:
			dateendidx[intdt] = i
		h0 = hash(records['date'][i])
		h1 = hash(records['portfolio'][i])
		h2 = hash(records['symbol'][i])
		h = (h0^h1^h2)%n
		if pkey[h] == -1:
			pkey[h] = i
		else:
			duplicatedkey=True
			j=1
			while (\
				(records[pkey[h]]['date'] != records[i]['date']) |
				(records[pkey[h]]['portfolio'] != records[i]['portfolio']) |
				(records[pkey[h]]['symbol'] != records[i]['symbol'])
			):
				h = (h + j**2) % n
				if pkey[h]==-1:
					pkey[h]=i
					duplicatedkey=False
					break
				j+=1
			if duplicatedkey:
				raise Exception('error duplicated index')

		hport = (h0^h1)%n
		if portiniidx[hport] == -1:
			newid = int(portlistcount*2)
			portiniidx[hport] = newid
			portendidx[hport] = newid
			portlist[newid]=i
			portlistcount+=1
		else:
			j=1
			fid=portlist[portiniidx[hport]]
			newindex = False
			while (\
				(records[fid]['date'] != records[i]['date']) |
				(records[fid]['portfolio'] != records[i]['portfolio'])
			):
				hport = (hport + j**2) % n
				if portiniidx[hport]==-1:
					newid = int(portlistcount*2)
					portiniidx[hport] = newid
					portendidx[hport] = newid
					portlist[newid]=i
					portlistcount+=1
					newindex = True
					break
				fid=portlist[portiniidx[hport]]
				j+=1
			if not newindex:
				curid = portendidx[hport]
				newid = int(portlistcount*2)
				portlist[curid+1]=newid
				portlist[newid]=i
				portendidx[hport] = newid
				portlistcount+=1

@njit(cache=True)
def get_loc_date_portfolio_symbol_jit(records,pkey,keys):
	n = pkey.size-1
	loc = np.empty((keys.size, ))
	for i in range(keys.size):
		h0 = hash(keys['date'][i])
		h1 = hash(keys['portfolio'][i])
		h2 = hash(keys['symbol'][i])
		h = (h0^h1^h2)%n
		if pkey[h] == -1:
			loc[i] = pkey[h]
		else:
			j=1
			while (\
				(records[pkey[h]]['date'] != keys[i]['date']) |
				(records[pkey[h]]['portfolio'] != keys[i]['portfolio']) |
				(records[pkey[h]]['symbol'] != keys[i]['symbol'])
			):
				h = (h + j**2) % n
				if pkey[h]==-1:
					break
				j+=1
			loc[i]=pkey[h]
	return loc

@njit(cache=True)
def upsert_date_portfolio_symbol_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,portiniidx,portendidx,portlist,portlistcount):
	minchgid = count
	maxsize = records.size
	nrec = new_records.size
	loc = get_loc_date_portfolio_symbol_jit(records, pkey, new_records)
	# new items
	isnew = new_records[loc==-1]
	if isnew.size > 0:
		minchgid = int(count)
		addsize = min(maxsize - count, isnew.size)
		count += addsize
		records[minchgid:count] = isnew[0:addsize]
		create_pkey_date_portfolio_symbol_jit(records,count,pkey,dateiniidx,dateendidx,dateunit,portiniidx,portendidx,portlist,portlistcount,minchgid)
	# existing items
	if isnew.size < nrec:
		minchgid = min(loc[loc>-1])
		for i in range(nrec):
			if loc[i] != -1:
				records[int(loc[i])] = new_records[i]
	return count, minchgid

###################### DATE_PORTFOLIO_SYMBOL_CLORDID ########################
@njit(cache=True)
def create_pkey_date_portfolio_symbol_clordid_jit(records,count,pkey,dateiniidx,dateendidx,dateunit,portiniidx,portendidx,portlist,portlistcount,start):
	n = pkey.size-1
	for i in range(start,count):
		intdt = np.int32(np.int64(records['date'][i])/dateunit)
		if dateiniidx[intdt]==-1:
			dateiniidx[intdt] = i
		if dateendidx[intdt]<i:
			dateendidx[intdt] = i
		h0 = hash(records['date'][i])
		h1 = hash(records['portfolio'][i])
		h2 = hash(records['symbol'][i])
		h3 = hash(records['clordid'][i])
		h = (h0^h1^h2^h3)%n
		if pkey[h] == -1:
			pkey[h] = i
		else:
			duplicatedkey=True
			j=1
			while (\
				(records[pkey[h]]['date'] != records[i]['date']) |
				(records[pkey[h]]['portfolio'] != records[i]['portfolio']) |
				(records[pkey[h]]['symbol'] != records[i]['symbol']) |
				(records[pkey[h]]['clordid'] != records[i]['clordid'])
			):
				h = (h + j**2) % n
				if pkey[h]==-1:
					pkey[h]=i
					duplicatedkey=False
					break
				j+=1
			if duplicatedkey:
				raise Exception('error duplicated index')

		hport = (h0^h1)%n
		if portiniidx[hport] == -1:
			newid = int(portlistcount*2)
			portiniidx[hport] = newid
			portendidx[hport] = newid
			portlist[newid]=i
			portlistcount+=1
		else:
			j=1
			fid=portlist[portiniidx[hport]]
			newindex = False
			while (\
				(records[fid]['date'] != records[i]['date']) |
				(records[fid]['portfolio'] != records[i]['portfolio'])
			):
				hport = (hport + j**2) % n
				if portiniidx[hport]==-1:
					newid = int(portlistcount*2)
					portiniidx[hport] = newid
					portendidx[hport] = newid
					portlist[newid]=i
					portlistcount+=1
					newindex = True
					break
				fid=portlist[portiniidx[hport]]
				j+=1
			if not newindex:
				curid = portendidx[hport]
				newid = int(portlistcount*2)
				portlist[curid+1]=newid
				portlist[newid]=i
				portendidx[hport] = newid
				portlistcount+=1

@njit(cache=True)
def get_loc_date_portfolio_symbol_clordid_jit(records,pkey,keys):
	n = pkey.size-1
	loc = np.empty((keys.size, ))
	for i in range(keys.size):
		h0 = hash(keys['date'][i])
		h1 = hash(keys['portfolio'][i])
		h2 = hash(keys['symbol'][i])
		h3 = hash(keys['clordid'][i])
		h = (h0^h1^h2^h3)%n
		if pkey[h] == -1:
			loc[i] = pkey[h]
		else:
			j=1
			while (\
				(records[pkey[h]]['date'] != keys[i]['date']) |
				(records[pkey[h]]['portfolio'] != keys[i]['portfolio']) |
				(records[pkey[h]]['symbol'] != keys[i]['symbol']) |
				(records[pkey[h]]['clordid'] != keys[i]['clordid'])
			):
				h = (h + j**2) % n
				if pkey[h]==-1:
					break
				j+=1
			loc[i]=pkey[h]
	return loc

@njit(cache=True)
def upsert_date_portfolio_symbol_clordid_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,portiniidx,portendidx,portlist,portlistcount):
	minchgid = count
	maxsize = records.size
	nrec = new_records.size
	loc = get_loc_date_portfolio_symbol_clordid_jit(records, pkey, new_records)
	# new items
	isnew = new_records[loc==-1]
	if isnew.size > 0:
		minchgid = int(count)
		addsize = min(maxsize - count, isnew.size)
		count += addsize
		records[minchgid:count] = isnew[0:addsize]
		create_pkey_date_portfolio_symbol_clordid_jit(records,count,pkey,dateiniidx,dateendidx,dateunit,portiniidx,portendidx,portlist,portlistcount,minchgid)
	# existing items
	if isnew.size < nrec:
		minchgid = min(loc[loc>-1])
		for i in range(nrec):
			if loc[i] != -1:
				records[int(loc[i])] = new_records[i]
	return count, minchgid

###################### DATE_PORTFOLIO_SYMBOL_TRADEID ########################
@njit(cache=True)
def create_pkey_date_portfolio_symbol_tradeid_jit(records,count,pkey,dateiniidx,dateendidx,dateunit,portiniidx,portendidx,portlist,portlistcount,start):
	n = pkey.size-1
	for i in range(start,count):
		intdt = np.int32(np.int64(records['date'][i])/dateunit)
		if dateiniidx[intdt]==-1:
			dateiniidx[intdt] = i
		if dateendidx[intdt]<i:
			dateendidx[intdt] = i
		h0 = hash(records['date'][i])
		h1 = hash(records['portfolio'][i])
		h2 = hash(records['symbol'][i])
		h3 = hash(records['tradeid'][i])
		h = (h0^h1^h2^h3)%n
		if pkey[h] == -1:
			pkey[h] = i
		else:
			duplicatedkey=True
			j=1
			while (\
				(records[pkey[h]]['date'] != records[i]['date']) |
				(records[pkey[h]]['portfolio'] != records[i]['portfolio']) |
				(records[pkey[h]]['symbol'] != records[i]['symbol']) |
				(records[pkey[h]]['tradeid'] != records[i]['tradeid'])
			):
				h = (h + j**2) % n
				if pkey[h]==-1:
					pkey[h]=i
					duplicatedkey=False
					break
				j+=1
			if duplicatedkey:
				raise Exception('error duplicated index')

		hport = (h0^h1)%n
		if portiniidx[hport] == -1:
			newid = int(portlistcount*2)
			portiniidx[hport] = newid
			portendidx[hport] = newid
			portlist[newid]=i
			portlistcount+=1
		else:
			j=1
			fid=portlist[portiniidx[hport]]
			newindex = False
			while (\
				(records[fid]['date'] != records[i]['date']) |
				(records[fid]['portfolio'] != records[i]['portfolio'])
			):
				hport = (hport + j**2) % n
				if portiniidx[hport]==-1:
					newid = int(portlistcount*2)
					portiniidx[hport] = newid
					portendidx[hport] = newid
					portlist[newid]=i
					portlistcount+=1
					newindex = True
					break
				fid=portlist[portiniidx[hport]]
				j+=1
			if not newindex:
				curid = portendidx[hport]
				newid = int(portlistcount*2)
				portlist[curid+1]=newid
				portlist[newid]=i
				portendidx[hport] = newid
				portlistcount+=1

@njit(cache=True)
def get_loc_date_portfolio_symbol_tradeid_jit(records,pkey,keys):
	n = pkey.size-1
	loc = np.empty((keys.size, ))
	for i in range(keys.size):
		h0 = hash(keys['date'][i])
		h1 = hash(keys['portfolio'][i])
		h2 = hash(keys['symbol'][i])
		h3 = hash(keys['tradeid'][i])
		h = (h0^h1^h2^h3)%n
		if pkey[h] == -1:
			loc[i] = pkey[h]
		else:
			j=1
			while (\
				(records[pkey[h]]['date'] != keys[i]['date']) |
				(records[pkey[h]]['portfolio'] != keys[i]['portfolio']) |
				(records[pkey[h]]['symbol'] != keys[i]['symbol']) |
				(records[pkey[h]]['tradeid'] != keys[i]['tradeid'])
			):
				h = (h + j**2) % n
				if pkey[h]==-1:
					break
				j+=1
			loc[i]=pkey[h]
	return loc

@njit(cache=True)
def upsert_date_portfolio_symbol_tradeid_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,portiniidx,portendidx,portlist,portlistcount):
	minchgid = count
	maxsize = records.size
	nrec = new_records.size
	loc = get_loc_date_portfolio_symbol_tradeid_jit(records, pkey, new_records)
	# new items
	isnew = new_records[loc==-1]
	if isnew.size > 0:
		minchgid = int(count)
		addsize = min(maxsize - count, isnew.size)
		count += addsize
		records[minchgid:count] = isnew[0:addsize]
		create_pkey_date_portfolio_symbol_tradeid_jit(records,count,pkey,dateiniidx,dateendidx,dateunit,portiniidx,portendidx,portlist,portlistcount,minchgid)
	# existing items
	if isnew.size < nrec:
		minchgid = min(loc[loc>-1])
		for i in range(nrec):
			if loc[i] != -1:
				records[int(loc[i])] = new_records[i]
	return count, minchgid

####################### COMPOSITE INDEX ######################################
from numba.typed import List
@njit(cache=True)
def get_index_date_portfolio_jit(records,keys,pkey,portiniidx,portlist):
	n = pkey.size-1
	loc = List()
	keyloc = List()
	for i in range(keys.size):
		h0 = hash(keys['date'][i])
		h1 = hash(keys['portfolio'][i])		
		h = (h0^h1)%n
		if portiniidx[h] == -1:
			pass
		else:
			j=1
			portfound=True
			recid = portlist[portiniidx[h]]
			while (\
				(records[recid]['date'] != keys[i]['date']) |
				(records[recid]['portfolio'] != keys[i]['portfolio'])				
			):
				h = (h + j**2) % n
				if portiniidx[h]==-1:
					portfound=False
					break
				recid = portlist[portiniidx[h]]
				j+=1
			if portfound:
				curid = portiniidx[h]
				fid = portlist[curid]
				loc.append(fid)
				keyloc.append(i)
				nextid = portlist[curid+1]
				while nextid!=-1:
					curid = nextid
					loc.append(portlist[curid])
					keyloc.append(i)
					nextid = portlist[curid+1]
	return loc,keyloc
