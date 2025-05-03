package loader

type Unique[k string, v any] struct {
	buf map[k]v
}

func NewUnique[k string, v any]() *Unique[k, v] {
	return &Unique[k, v]{
		buf: make(map[k]v),
	}
}

func (u *Unique[k, v]) Insert(key k, val v) {
	_, exist := u.buf[key]
	if !exist {
		u.buf[key] = val
	}
}

func (u *Unique[k, v]) Get() []v {
	val := make([]v, 0, len(u.buf))

	for _, uv := range u.buf {
		val = append(val, uv)
	}

	return val
}
